# Usage

## Basic Example

Here's a simple example of how to use pypdown:

```python
from pypdown import run_step
from pypdown.models import Step
from pydantic import BaseModel
from pathlib import Path

class StepParams(BaseModel):
    input_file: Path = "input.txt"
    output_file: Path = "output.txt"
    final_file: Path = "final.txt"

def process_input(input_file: Path, output_file: Path, config: StepParams):
    """Process input file and create output file."""
    output_file.write_text(input_file.read_text().upper())

def finalize_output(output_file: Path, final_file: Path, config: StepParams):
    """Process output file and create final file."""
    final_file.write_text(f"Processed: {output_file.read_text()}")

config = StepParams()

# Define your pipeline tasks
tasks = [
    {
        "src": config.model_dump(include=["input_file"]),
        "dst": config.model_dump(include=["output_file"]),
        "fn": process_input,
    },
    {
        "src": config.model_dump(include=["output_file"]),
        "dst": config.model_dump(include=["final_file"]),
        "fn": finalize_output,
    },
]

# Create a Step
step = Step(name="My Pipeline", tasks=tasks, config=config)

# Run the step
run_step(step)
```

This will create a pipeline that reads from `input.txt`, processes it to create `output.txt`, and then processes `output.txt` to create `final.txt`.

## Defining Tasks

Tasks have three components:

- `src`: A dictionary of input file paths
- `dst`: A dictionary of output file paths
- `fn`: A callback function that performs the task

You should create the dictionaries from a Pydantic model's field names to the field values.

## Callback Functions

Callback functions should take the input and output file paths as keyword arguments,
along with a `config` parameter for the Pydantic model that all the parameters are set from.

## Running Steps

Use the `run_step` function to execute a pipeline step.
This function will check for the existence of input files and the non-existence of output files before running each task.

For full implementation details, please refer to the [API Reference](../api/index.md).
