from pathlib import Path

from pydantic import BaseModel

from pypdown import run_step
from pypdown.models import Step


def test_long_example(tmp_path: Path):
    class StepParams(BaseModel):
        n1_o: Path
        n2_o: Path
        a_i: Path
        a_o: Path
        b_o: Path
        c_o: Path
        d_i: Path
        d_o: Path
        e_i: Path
        e_o: Path

    # Build all paths inside tmp dir
    config = StepParams(
        n1_o=tmp_path / "nil1.out",
        n2_o=tmp_path / "nil2.out",
        a_i=tmp_path / "a.in",
        a_o=tmp_path / "a.out",
        b_o=tmp_path / "b.out",
        c_o=tmp_path / "c.out",
        d_i=tmp_path / "d.in",
        d_o=tmp_path / "d.out",
        e_i=tmp_path / "e.in",
        e_o=tmp_path / "e.out",
    )

    # Create required input files
    config.a_i.touch()
    config.d_i.touch()
    config.e_i.touch()

    def cb_n1(n1_o: Path, config: StepParams):
        n1_o.touch()

    def cb_a(a_i: Path, a_o: Path, config: StepParams):
        assert a_i.exists()
        a_o.touch()

    def cb_b(a_o: Path, b_o: Path, config: StepParams):
        assert a_o.exists()
        b_o.touch()

    def cb_c(a_o: Path, b_o: Path, c_o: Path, config: StepParams):
        assert a_o.exists() and b_o.exists()
        c_o.touch()

    def cb_d(d_i: Path, d_o: Path, config: StepParams):
        assert d_i.exists()
        d_o.touch()

    def cb_e(e_i: Path, e_o: Path, config: StepParams):
        assert e_i.exists()
        e_o.touch()

    def cb_n2(n2_o: Path, config: StepParams):
        n2_o.touch()

    task_fields = [
        ([], ["n1_o"], cb_n1),
        (["a_i"], ["a_o"], cb_a),
        (["a_o"], ["b_o"], cb_b),
        (["a_o", "b_o"], ["c_o"], cb_c),
        (["d_i"], ["d_o"], cb_d),
        (["e_i"], ["e_o"], cb_e),
        ([], ["n2_o"], cb_n2),
    ]

    task_refs = [
        dict(src=inputs, dst=outputs, fn=fn) for inputs, outputs, fn in task_fields
    ]

    step = Step(name="Large Step", task_refs=task_refs, config=config)
    run_step(step)
