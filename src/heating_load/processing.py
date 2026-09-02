"""Post-process EnergyPlus tabular output without changing the study method."""

from typing import Any

import pandas as pd

MONTHLY_COLUMNS = ("month", "electricity:facility,Meter", "gas:facility,Meter")


def aggregate_monthly_loads(data: Any) -> pd.DataFrame:
    """Group facility electricity and gas meter values by month.

    This is the same column selection and sum operation used by the original
    notebooks. The year supplied to opyplus remains an execution concern.
    """
    frame = pd.DataFrame(data)
    missing = [column for column in MONTHLY_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError("EnergyPlus output is missing columns: " + ", ".join(missing))
    return frame.loc[:, MONTHLY_COLUMNS].groupby("month", sort=True).sum(numeric_only=True)
