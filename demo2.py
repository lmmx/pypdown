from pypdown import run_step
from pypdown.models import Step
from pydantic import BaseModel
from pathlib import Path

class StepParams(BaseModel):
    a1_i: Path = "a1.in"
    a2_i: Path = "a2.in"
    a_o: Path = "a.out"
    b_i: Path = "b.in"
    b_o: Path = "b.out"

config = StepParams()


file_tasks = [
    (["a1_i", "a2_i"], ["a_o"]),
    (["a_o", "b_i"], ["b_o"]),
]

# Turn the in/output lists into dicts keyed by config field name with filename values
named_file_tasks = [
    tuple({field: getattr(config, field) for field in files} for files in task)
    for task in file_tasks
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in named_file_tasks])
run_step(step)
