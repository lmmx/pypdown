from pypdown import run_step
from pypdown.models import Step

file_tasks = [
    (["a1.in", "a2.in"], ["a.out"]),
    (["a.out", "b.in"], ["b.out"]),
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in file_tasks])
run_step(step)
