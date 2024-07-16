from pypdown import run_step

file_tasks = [
    ([], ["nil1.out"]),
    (["a.in"], ["a.out"]),
    (["a.out"], ["b.out"]),
    (["a.out", "b.out"], ["c.out"]),
    (["d.in"], ["d.out"]),
    (["e.in"], ["e.out"]),
    ([], ["nil2.out"]),
]

run_step(file_tasks)
