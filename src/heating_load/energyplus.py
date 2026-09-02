"""Optional EnergyPlus/opyplus integration."""

from pathlib import Path
from typing import Any

from .config import Case


def run_case(case: Case, output_dir: Path, energyplus_version: tuple[int, int, int] = (9, 2, 0)) -> Any:
    """Run one case through opyplus and return its simulation object.

    opyplus is imported only when this function is called so input processing
    and unit tests remain usable without an EnergyPlus installation.
    """
    try:
        import opyplus as op
    except ImportError as exc:
        raise RuntimeError("opyplus is required to run EnergyPlus simulations") from exc

    if not case.idf_path.is_file() or not case.epw_path.is_file():
        raise FileNotFoundError("Case input files must exist before simulation")
    output_dir.mkdir(parents=True, exist_ok=True)
    simulation = op.simulate(
        str(case.idf_path),
        str(case.epw_path),
        str(output_dir),
        simulation_name=None,
        print_function=None,
        beat_freq=None,
    )
    return simulation


def monthly_loads(simulation: Any, weather_year: int) -> Any:
    """Extract and aggregate the notebook's monthly meter output."""
    hourly_output = simulation.get_out_eso()
    hourly_output.create_datetime_index(weather_year)
    from .processing import aggregate_monthly_loads

    return aggregate_monthly_loads(hourly_output.get_data())
