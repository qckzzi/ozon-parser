from dataclasses import dataclass


@dataclass(slots=True)
class Characteristic:
    name: str
    value: str
