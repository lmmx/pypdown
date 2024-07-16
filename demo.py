from pypdown import run_step
from pypdown.models import Step

file_tasks = [
    ([], ["nil1.out"]),
    (["a.in"], ["a.out"]),
    (["a.out"], ["b.out"]),
    (["a.out", "b.out"], ["c.out"]),
    (["d.in"], ["d.out"]),
    (["e.in"], ["e.out"]),
    ([], ["nil2.out"]),
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in file_tasks])
run_step(step)
