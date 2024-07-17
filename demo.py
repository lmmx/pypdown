from pypdown import run_step
from pypdown.models import Step
from pydantic import BaseModel
from pathlib import Path

class StepParams(BaseModel):
    n1_o: Path = "nil1.out"
    n2_o: Path = "nil2.out"
    a_i: Path = "a.in"
    a_o: Path = "a.out"
    b_o: Path = "b.out"
    c_o: Path = "c.out"
    d_i: Path = "d.in"
    d_o: Path = "d.out"
    e_i: Path = "e.in"
    e_o: Path = "e.out"

config = StepParams()

file_tasks = [
    ([], ["n1_o"]),
    (["a_i"], ["a_o"]),
    (["a_o"], ["b_o"]),
    (["a_o", "b_o"], ["c_o"]),
    (["d_i"], ["d_o"]),
    (["e_i"], ["e_o"]),
    ([], ["n2_o"]),
]

# Turn the in/output lists into dicts keyed by config field name with filename values
named_file_tasks = [
    tuple({field: getattr(config, field) for field in files} for files in task)
    for task in file_tasks
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in named_file_tasks])
run_step(step)
