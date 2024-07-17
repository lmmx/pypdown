from pypdown import run_step
from pypdown.models import Step

file_tasks = [
    (["a1.in", "a2.in"], ["a.out"]),
    (["a.out", "b.in"], ["b.out"]),
]

# Turn the in/output lists into dicts keyed by _-slugged filename
named_file_tasks = [
    tuple({file.replace('.', '_'): file for file in files} for files in task)
    for task in file_tasks
]

step = Step(name="Demo Step", tasks=[{"src": s, "dst": d} for s, d in named_file_tasks])
run_step(step)
