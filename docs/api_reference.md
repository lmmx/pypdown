# API Reference

## `pypdown.models`

### `Task`

```python
class Task(BaseModel):
    src: list[Path]
    dst: list[Path]
```

Represents a task with input (`src`) and output (`dst`) files.

### `Step`

```python
class Step(BaseModel):
    name: str
    tasks: list[Task]
```

Represents a named step in a data pipeline, consisting of multiple tasks.

## `pypdown.run`

### `run_step`

```python
def run_step(step: Step):
    ...
```

Executes a pipeline step, checking for file existence and running tasks accordingly.

For more detailed information on each component, please refer to the source code and inline documentation.
