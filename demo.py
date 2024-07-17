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

# Turn the in/output lists into dicts keyed by _-slugged filename
named_file_tasks = [
    tuple({file.replace('.', '_'): file for file in files} for files in task)
    for task in file_tasks
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in named_file_tasks])
run_step(step)
