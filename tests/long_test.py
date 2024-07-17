from pathlib import Path

from pydantic import BaseModel
from pypdown import run_step
from pypdown.models import Step


def test_long_example():
    class StepParams(BaseModel):
        n1_o: Path = "nil1.out"
        n2_o: Path = "nil2.out"
        a_i: Path = "a.in"
        a_o: Path = "a.out"
        b_o: Path = "b.out"
        c_o: Path = "c.out"
        d_i: Path = "d.in"
        d_o: Path = "d.out"
        e_i: Path = "e.in"
        e_o: Path = "e.out"

    config = StepParams()

    def cb_n1(n1_o: Path, config: StepParams):
        n1_o.touch()
        print(f"Touched {n1_o=}")

    def cb_a(a_i: Path, a_o: Path, config: StepParams):
        assert a_i.exists()
        a_o.touch()
        print(f"Touched {a_o=}")

    def cb_b(a_o: Path, b_o: Path, config: StepParams):
        assert a_o.exists()
        b_o.touch()
        print(f"Touched {b_o=}")

    def cb_c(a_o: Path, b_o: Path, c_o: Path, config: StepParams):
        assert a_o.exists() and b_o.exists()
        c_o.touch()
        print(f"Touched {c_o=}")

    def cb_d(d_i: Path, d_o: Path, config: StepParams):
        assert d_i.exists()
        d_o.touch()
        print(f"Touched {d_o=}")

    def cb_e(e_i: Path, e_o: Path, config: StepParams):
        assert e_i.exists()
        e_o.touch()
        print(f"Touched {e_o=}")

    def cb_n2(n2_o: Path, config: StepParams):
        n2_o.touch()
        print(f"Touched {n2_o=}")

    task_fields = [
        ([], ["n1_o"], cb_n1),
        (["a_i"], ["a_o"], cb_a),
        (["a_o"], ["b_o"], cb_b),
        (["a_o", "b_o"], ["c_o"], cb_c),
        (["d_i"], ["d_o"], cb_d),
        (["e_i"], ["e_o"], cb_e),
        ([], ["n2_o"], cb_n2),
    ]

    # Turn the in/output lists into dicts keyed by config field name with filename values
    task_refs = [
        dict(src=inputs, dst=outputs, fn=fn) for inputs, outputs, fn in task_fields
    ]

    step = Step(name="Large Step", task_refs=task_refs, config=config)
    run_step(step)
