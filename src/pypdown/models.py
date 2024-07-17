"""Pydantic models to represent the tasks within a step in a data pipeline."""

from pathlib import Path
from typing import TypeVar
from collections.abc import Callable

from pydantic import BaseModel, FilePath, NewPath, OnErrorOmit, TypeAdapter

__all__ = [
    "AvailableTask",
    "CompletedTask",
    "Task",
    "Step",
    "AvailableTA",
    "CompletedTA",
    "RunContext",
]


class Executable(BaseModel):
    """All tasks must have an associated function to make them executable."""

    fn: Callable


class AvailableTask(Executable):
    """A task is available when its input files exist and its outputs don't."""

    src: dict[str, FilePath]
    dst: dict[str, NewPath]


class CompletedTask(Executable):
    """A task is completed when its output files exist, whether inputs exist or not."""

    src: dict[str, Path]
    dst: dict[str, FilePath]


class Task(Executable):
    """A task has zero or more input files and zero or more output files."""

    src: dict[str, Path]
    dst: dict[str, Path]


C = TypeVar("C", bound=BaseModel)


class Step(BaseModel):
    """A named step in a data pipeline, split up into tasks with specified file I/O."""

    name: str
    tasks: list[Task]
    config: C


AvailableTA = TypeAdapter(list[OnErrorOmit[AvailableTask]])
CompletedTA = TypeAdapter(list[OnErrorOmit[CompletedTask]])


class RunContext(BaseModel):
    """The context available to a task runner."""

    step: Step
    idx: int
