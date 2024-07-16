# Usage

## Basic Example

Here's a simple example of how to use pypdown:

```python
from pypdown import run_step
from pypdown.models import Step

# Define your pipeline tasks
tasks = [
    (["input.txt"], ["output.txt"]),
    (["output.txt"], ["final.txt"]),
]

# Create a Step
step = Step(name="My Pipeline", tasks=[{"src": s, "dst": d} for s, d in tasks])

# Run the step
run_step(step)
```

This will create a pipeline that reads from `input.txt`, processes it to create `output.txt`, and then processes `output.txt` to create `final.txt`.

## Defining Tasks

Tasks are defined as tuples of input and output files. The first element of the tuple is a list of input files, and the second element is a list of output files.

## Running Steps

Use the `run_step` function to execute a pipeline step. This function will check for the existence of input files and the non-existence of output files before running each task.

For more advanced usage, please refer to the [API Reference](../api/index.md).
