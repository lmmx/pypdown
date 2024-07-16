# pypdown

A Pydantic model-based approach to data pipelining with file I/O linting.

[![PyPI version](https://badge.fury.io/py/pypdown.svg)](https://badge.fury.io/py/pypdown)
[![Python Versions](https://img.shields.io/pypi/pyversions/pypdown.svg)](https://pypi.org/project/pypdown/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/pypdown/badge/?version=latest)](https://pypdown.readthedocs.io/en/latest/?badge=latest)
![GitHub Actions](https://github.com/lmmx/pypdown/actions/workflows/ci/badge.svg)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/pypdown/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/pypdown/master)

## Features

- Pydantic model-based approach to data pipelining
- File I/O linting for robust pipeline execution
- Easy-to-use API for defining and running pipeline steps

## Installation

```bash
pip install pypdown
```

## Quick Start

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

## Documentation

For full documentation, please visit [pypdown.readthedocs.io](https://pypdown.readthedocs.io).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
