"""Main module."""

from enum import Enum

from pydantic.dataclasses import dataclass


class Side(Enum):
    LEFT = "left"
    RIGHT = "right"
    BOTH = ""


@dataclass
class WorkoutSet:
    order: int
    name: str
    duration: int
    side: str
    description: str
