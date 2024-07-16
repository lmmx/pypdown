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


file_tasks = [
    ([], ["nil1.out"]),
    (["a.in"], ["a.out"]),
    (["a.out"], ["b.out"]),
    (["a.out", "b.out"], ["c.out"]),
    (["d.in"], ["d.out"]),
    (["e.in"], ["e.out"]),
    ([], ["nil2.out"]),
]

available_ta = TypeAdapter(list[OnErrorOmit[AvailableTask]])
completed_ta = TypeAdapter(list[OnErrorOmit[CompletedTask]])


def run_step():
    tasks = [dict(src=s, dst=d) for s, d in file_tasks]
    step = Step(name="Demo Step", tasks=tasks)

    if step.tasks:
        print(f"Running step {step.name!r} with {len(step.tasks)} tasks")
    else:
        raise ValueError("No tasks were assigned")

    task_picked_up = False
    bail = False
    for idx, task in enumerate(step.tasks):
        task_repr = " --> ".join(map(str, (task.model_dump(mode="json").values())))
        print(
            f"\n--- Task {idx + 1} --- Prepared task\n{'':15}{task_repr}\n",
            end=f"{'':10}",
        )
        if bail:
            print(f" (-) Bailing out of step, skipping task")
            continue
        available = available_ta.validate_python([task.model_dump()])
        completed = completed_ta.validate_python([task.model_dump()])
        if available:
            print(f" \033[92;1m>>>\033[0m Running available task")
            task_picked_up = True
        else:
            if task_picked_up:
                print(f" (x) Task already completed, skipping")
            else:
                print(f" (!) Task requisite missing, bailing")
                bail = True
