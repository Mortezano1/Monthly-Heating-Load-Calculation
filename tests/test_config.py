from pathlib import Path

import pytest

from heating_load.config import Orientation, available_cases, resolve_case


@pytest.fixture()
def project_root(tmp_path: Path) -> Path:
    data = tmp_path / "Data"
    data.mkdir()
    for name in (
        "DOEE-EnergyPlus V0.1.2(EAST).idf",
        "DOEE-EnergyPlus V0.1.2(NORTH).idf",
        "DOEE-EnergyPlus V0.1.2(SOUTH).idf",
        "DOEE-EnergyPlus V0.1.2(W).idf",
        "IRN_ES_Kashan.AP.407850_TMYx.2004-2018.epw",
        "IRN_Tabriz.407060_ITMY.epw",
        "IRN_Tehran-Mehrabad.407540_ITMY.epw",
    ):
        (data / name).touch()
    return tmp_path


def test_resolve_case_uses_repository_inputs(project_root: Path) -> None:
    case = resolve_case(project_root, "tehran", "north")
    assert case.orientation is Orientation.NORTH
    assert case.epw_path.name == "IRN_Tehran-Mehrabad.407540_ITMY.epw"


def test_available_cases_contains_all_combinations(project_root: Path) -> None:
    assert len(available_cases(project_root)) == 12


def test_missing_input_is_reported(project_root: Path) -> None:
    (project_root / "Data/DOEE-EnergyPlus V0.1.2(EAST).idf").unlink()
    with pytest.raises(FileNotFoundError, match="EAST"):
        resolve_case(project_root, "Kashan", "East")
