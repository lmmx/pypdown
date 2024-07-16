from .models import AvailableTA, CompletedTA, Step

__all__ = ["run_step"]


def run_step(step: Step):
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

        available = AvailableTA.validate_python([task.model_dump()])
        completed = CompletedTA.validate_python([task.model_dump()])

        if available:
            print(" \033[92;1m>>>\033[0m Running available task")
        elif completed:
            print(" (x) Task already completed, skipping")
        else:
            print(" (!) Task requisite missing, bailing")
            bail = True
