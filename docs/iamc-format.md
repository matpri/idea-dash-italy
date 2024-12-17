# IAMC Format Documentation

## Overview

The IAMC (Integrated Assessment Modeling Consortium) format is a standardized data structure used for organizing and
sharing model output and scenario data across various research groups and institutions. The format facilitates the
comparison, aggregation, and analysis of data from different models by enforcing a consistent structure for reporting
variables, regions, and time periods.

In this specific version of the IAMC format, instead of having a separate column for each year, the data is organized
with a single `time` column. This approach simplifies the format, making it easier to handle datasets with varying time
steps (e.g., annual, monthly) and to perform time-series analysis.

## Columns Description

### `model`

- **Description:** The name of the model used to generate the data.
- **Example:** `COPPER`

### `scenario`

- **Description:** The name of the scenario under which the data was generated. Scenarios often represent different
  assumptions about future developments, such as policy interventions or technological advancements.
- **Example:** `BAU`

### `region`

- **Description:** The geographical region to which the data applies. This could be subregions of a country, a country,
  a group of countries, or a global region.
- **Example:** `British Columbia`, `Alberta`, `Canada`, `World`

### `variable`

- **Description:** The variable or metric being reported, such as energy production, emissions, or GDP. Variables are
  often hierarchical and can include subcategories. If no custom profile was defined, the highest level of the variable hierarchy will be used to distinguish between different types of data and plots will be automatically generated for each distinct variable.
- **Example:** `Emissions|CO2`, `Total Capacity|Coal` (in this case IDEA would generate a plot for Emissions and another for Total Capacity if no custom profile was implemented for the model)

### `unit`

- **Description:** The unit of measurement for the variable. The unit is crucial for ensuring that data from different
  sources can be accurately compared.
- **Example:** `MtCO2`, `MW`

### `time`

- **Description:** The time point associated with the reported data. In this version of the IAMC format, all time points
  are reported in a single column, which allows for flexible time-series data representation.
- **Example:** `2025`, `2030`, `2050`, (datetime format is also allowed for a more detailed
  timeseries) `2025-01-01`, `2025-02-01 12:00:00`

### `value`

- **Description:** The numerical value associated with the specific combination
  of `model`, `scenario`, `region`, `variable`, `unit`, and `time`.
- **Example:** `500`, `12000`

### Optional Columns

The IAMC format allows for additional columns to be included in the dataset to provide more context or metadata about
the data. These columns can include information such as the author of the data, the source of the data, or additional
notes about the data generation process. For _SILVER_
we include the bus location using their coordinates as additional information for plots

## Example

Here's a sample entry in the IAMC format:

| model  | scenario | region           | variable              | unit  | time | value |
|--------|----------|------------------|-----------------------|-------|------|-------|
| COPPER | BAU      | British Columbia | Emissions\| Coal      | MtCO2 | 2025 | 45000 |
| COPPER | BAU      | British Columbia | Total Capacity\| Coal | MW    | 2025 | 120   |

This format is designed to be simple yet flexible, allowing researchers to efficiently handle large datasets with
varying time steps and provide clear, consistent data for integrated assessment modeling.

