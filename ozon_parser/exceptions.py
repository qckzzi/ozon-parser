class PagesCountNotFoundError(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f"Pages count at {url=} not found")
