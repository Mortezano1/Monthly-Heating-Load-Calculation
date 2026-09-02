import pandas as pd
import pytest

from heating_load.processing import aggregate_monthly_loads


def test_aggregate_monthly_loads_matches_notebook_operation() -> None:
    data = pd.DataFrame(
        {
            "month": [1, 1, 2],
            "electricity:facility,Meter": [2.0, 3.0, 4.0],
            "gas:facility,Meter": [5.0, 6.0, 7.0],
        }
    )
    result = aggregate_monthly_loads(data)
    assert result.loc[1, "electricity:facility,Meter"] == 5.0
    assert result.loc[2, "gas:facility,Meter"] == 7.0


def test_missing_meter_column_fails_clearly() -> None:
    with pytest.raises(ValueError, match="gas:facility,Meter"):
        aggregate_monthly_loads({"month": [1], "electricity:facility,Meter": [2]})
