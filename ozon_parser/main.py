import asyncio

from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue

from ozon_parser.container import Container


async def bake_container() -> None:
    await Container.aopen()


asyncio.run(bake_container())

broker: RabbitBroker = Container.broker()  # type: ignore[operator]
broker.include_router(Container.router())  # type: ignore[operator]
app = FastStream(broker)


@app.after_startup
async def on_startup() -> None:
    for queue in Container.queues_to_declare():  # type: ignore[operator]
        await broker.declare_queue(RabbitQueue(queue, durable=True))


@app.after_shutdown
async def on_shutdown() -> None:
    await Container.aclose()
