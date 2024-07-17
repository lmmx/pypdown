# pypdown

A Pydantic model-based approach to data pipelining with file I/O linting.

[![PyPI Version](https://img.shields.io/pypi/v/pypdown)](https://pypi.org/project/pypdown/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pypdown.svg)](https://pypi.org/project/pypdown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-pypdown.vercel.app-blue)](https://pypdown.vercel.app/)
[![CI Status](https://github.com/lmmx/pypdown/actions/workflows/ci.yml/badge.svg)](https://github.com/lmmx/pypdown/actions/workflows/ci.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/pypdown/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/pypdown/master)

## Features

- Pydantic model-based approach to data pipelining
- File I/O linting for robust pipeline execution
- Easy-to-use API for defining and running pipeline steps
- Support for callback functions and keyword argument-based file paths

## Installation

```bash
pip install pypdown
```

## Quick Start

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

# Define your pipeline tasks by reference to config field names
task_refs = [
    {
        "src": ["input_file"],
        "dst": ["output_file"],
        "fn": process_input,
    },
    {
        "src": ["output_file"],
        "dst": ["final_file"],
        "fn": finalize_output,
    },
]

# Create a Step
step = Step(name="Example Pipeline Step", task_refs=task_refs, config=config)

# Run the step
run_step(step)
```

## Documentation

For full documentation, please visit [pypdown.vercel.app](https://pypdown.vercel.app/).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
