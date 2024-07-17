"""Pydantic models to represent the tasks within a step in a data pipeline."""

from collections.abc import Callable
from pathlib import Path
from typing import TypeVar

from pydantic import (
    BaseModel,
    FilePath,
    NewPath,
    OnErrorOmit,
    TypeAdapter,
    computed_field,
)

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


class TaskRef(Executable):
    """A TaskRef is dereferenced to a Task by looking up src/dst fields on a config."""

    src: list[str]
    dst: list[str]


C = TypeVar("C", bound=BaseModel)


class Step(BaseModel):
    """A named step in a data pipeline, split up into tasks with specified file I/O."""

    name: str
    task_refs: list[TaskRef]
    config: C

    @computed_field
    @property
    def tasks(self) -> list[Task]:
        tasks = []
        for tr in self.task_refs:
            task = Task(
                src=self.config.model_dump(include=tr.src),
                dst=self.config.model_dump(include=tr.dst),
                fn=tr.fn,
            )
            # `model_dump(include=[...])` silently drops names missing not in the config
            assert not (no_src := set(tr.src) - set(task.src)), f"Not in src: {no_src}"
            assert not (no_dst := set(tr.dst) - set(task.dst)), f"Not in dst: {no_dst}"
        return tasks


AvailableTA = TypeAdapter(list[OnErrorOmit[AvailableTask]])
CompletedTA = TypeAdapter(list[OnErrorOmit[CompletedTask]])


class RunContext(BaseModel):
    """The context available to a task runner."""

    step: Step
    idx: int
