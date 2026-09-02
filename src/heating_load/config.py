"""Project-relative case and input path configuration."""

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class Orientation(StrEnum):
    EAST = "East"
    NORTH = "North"
    SOUTH = "South"
    WEST = "West"


@dataclass(frozen=True)
class Case:
    """A city/orientation simulation case and its repository inputs."""

    city: str
    orientation: Orientation
    idf_path: Path
    epw_path: Path


_CITY_WEATHER = {
    "Kashan": "IRN_ES_Kashan.AP.407850_TMYx.2004-2018.epw",
    "Tabriz": "IRN_Tabriz.407060_ITMY.epw",
    "Tehran": "IRN_Tehran-Mehrabad.407540_ITMY.epw",
}

_ORIENTATION_IDF_NAMES = {
    Orientation.EAST: "DOEE-EnergyPlus V0.1.2(EAST).idf",
    Orientation.NORTH: "DOEE-EnergyPlus V0.1.2(NORTH).idf",
    Orientation.SOUTH: "DOEE-EnergyPlus V0.1.2(SOUTH).idf",
    Orientation.WEST: "DOEE-EnergyPlus V0.1.2(W).idf",
}


def resolve_case(root: Path, city: str, orientation: str | Orientation) -> Case:
    """Resolve and validate one repository-local city/orientation case."""
    normalized_city = city.title()
    try:
        normalized_orientation = Orientation(str(orientation).title())
    except ValueError as exc:
        raise ValueError(f"Unsupported orientation: {orientation!r}") from exc
    try:
        weather_name = _CITY_WEATHER[normalized_city]
    except KeyError as exc:
        raise ValueError(f"Unsupported city: {city!r}") from exc

    data_dir = root / "Data"
    idf_path = data_dir / _ORIENTATION_IDF_NAMES[normalized_orientation]
    epw_path = data_dir / weather_name
    missing = [str(path) for path in (idf_path, epw_path) if not path.is_file()]
    if missing:
        raise FileNotFoundError("Required input file(s) not found: " + ", ".join(missing))
    return Case(normalized_city, normalized_orientation, idf_path, epw_path)


def available_cases(root: Path) -> list[Case]:
    """Return all validated city/orientation combinations in stable order."""
    return [
        resolve_case(root, city, orientation)
        for city in _CITY_WEATHER
        for orientation in Orientation
    ]
