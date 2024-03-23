FROM python:3.12.2-slim

RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-root

COPY src /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]