from pathlib import Path

from pydantic import BaseModel, FilePath, NewPath, OnErrorOmit, TypeAdapter


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


available_ta = TypeAdapter(list[OnErrorOmit[AvailableTask]])
completed_ta = TypeAdapter(list[OnErrorOmit[CompletedTask]])


def run_step(file_tasks: list[tuple[list[str], list[str]]]):
    tasks = [dict(src=s, dst=d) for s, d in file_tasks]
    step = Step(name="Demo Step", tasks=tasks)

    if step.tasks:
        print(f"Running step {step.name!r} with {len(step.tasks)} tasks")
    else:
        raise ValueError("No tasks were assigned")

    bail = False
    for idx, task in enumerate(step.tasks):
        task_repr = " --> ".join(map(str, (task.model_dump(mode="json").values())))
        print(
            f"\n--- Task {idx + 1} --- Prepared task\n{'':15}{task_repr}\n",
            end=f"{'':10}",
        )
        if bail:
            print(" (-) Bailing out of step, skipping task")
            continue

        available = available_ta.validate_python([task.model_dump()])
        completed = completed_ta.validate_python([task.model_dump()])

        if available:
            print(" \033[92;1m>>>\033[0m Running available task")
        elif completed:
            print(" (x) Task already completed, skipping")
        else:
            print(" (!) Task requisite missing, bailing")
            bail = True
