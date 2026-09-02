# Methodology

The original study combines EnergyPlus simulations with monthly post-processing associated with the ISO 13790 project scope. This refactor does not change the IDF models, weather files, meter names, formulas, or aggregation rule.

For each city and orientation, the workflow is:

1. Select the orientation-specific IDF model and city weather file.
2. Run EnergyPlus through `opyplus`.
3. Read the hourly ESO output.
4. Create the datetime index using the weather-year value supplied by the caller.
5. Select `electricity:facility,Meter` and `gas:facility,Meter`.
6. Sum those values by month.

The weather files are retained as supplied. The ITMY files do not provide enough evidence here to assign a calendar year, so the year is an explicit runtime parameter rather than an invented default. EnergyPlus warnings in historical notebook outputs also remain a model-review item; this repository does not claim they are harmless.
