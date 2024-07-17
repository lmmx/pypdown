"""Control flow using the Pydantic runtime file I/O checks."""

from .models import AvailableTA, AvailableTask, CompletedTA, Step, RunContext

__all__ = ["run_step"]


def task_runner(task: AvailableTask, context: RunContext) -> None:
    print(f"Hello world {task.model_dump(mode='json', exclude='fn')}")
    task.fn.__call__(**task.src, **task.dst, config=context.step.config)


def run_step(step: Step):
    """Run a pipeline step's tasks based on the availability of task files.

    Tasks are iterated through, and the relevant in/output files' existence existence
    is checked when the task is reached in the loop (rather than at the start). This
    means that intermediate files can be created by tasks, and their existence will be
    checked when those output files become inputs to subsequent tasks.

    If any task's required input files are missing, the step bails out: no further tasks
    will run.
    """
    if step.tasks:
        print(f"Running step {step.name!r} with {len(step.tasks)} tasks")
    else:
        raise ValueError("No tasks were assigned")

    bail = False
    for idx, task in enumerate(step.tasks):
        if idx > 0 and not bail:
            prev_task = step.tasks[idx - 1]
            prev_completed = CompletedTA.validate_python([prev_task.model_dump()])
            if not prev_completed:
                bail = True
                print("(!) Incomplete previous task detected, bailing")
        task_repr = " --> ".join(
            map(str, (task.model_dump(include=["src", "dst"], mode="json").values())),
        )
        print(f"\n--- Task {idx + 1} --- {task_repr}")
        if bail:
            print("(-) Bailing out of step, skipping task")
            continue

        available = AvailableTA.validate_python([task.model_dump()])
        completed = CompletedTA.validate_python([task.model_dump()])

        if available:
            print("\033[92;1m>>>\033[0m Running available task")
            task_runner(task=task, context=RunContext(step=step, idx=idx))
        elif completed:
            print("(x) Task already completed, skipping")
        else:
            print("(!) Task requisite missing, bailing")
            bail = True
