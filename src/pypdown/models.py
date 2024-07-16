"""Pydantic models to represent the tasks within a step in a data pipeline."""

from pathlib import Path

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


class AvailableTask(BaseModel):
    """A task is available when its input files exist and its outputs don't."""

    src: list[FilePath]
    dst: list[NewPath]


class CompletedTask(BaseModel):
    """A task is completed when its output files exist, whether inputs exist or not."""

    src: list[Path]
    dst: list[FilePath]


class Task(BaseModel):
    """A task has zero or more input files and zero or more output files."""

    src: list[Path]
    dst: list[Path]


class Step(BaseModel):
    """A named step in a data pipeline, split up into tasks with specified file I/O."""

    name: str
    tasks: list[Task]


AvailableTA = TypeAdapter(list[OnErrorOmit[AvailableTask]])
CompletedTA = TypeAdapter(list[OnErrorOmit[CompletedTask]])


class RunContext(BaseModel):
    """The context available to a task runner."""

    step: Step
    idx: int
