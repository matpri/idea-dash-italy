"""
===========================================================
Batch Update IDEA SK Emissions CSV Files

This script processes all matching scenario files in a folder:

1. Target files: *_results_general_IDEA_SK.csv
2. Source files: *_output_summary_IDEA_SK.csv

For each scenario:
- Matches target and source by scenario name in the filename.
- Filters source rows for Electricity emissions in Saskatchewan.
- Aggregates source totals (MtCO₂ → tonnes).
- Updates target rows where:
    - full_path == "CIMS.CAN.SK.Electricity"
    - parameter == "total_cumul_net_emissions"
  by assigning the aggregated total to CO2 rows.
- If no matching source data exists for a year/scenario, sets value_num to 0.
- Keeps all other rows unchanged.
- Saves updated CSV with "_updated" appended to the target filename.

Terminal output:
- Prints which rows were updated or zeroed (old → new).
- Shows summary of updated, zeroed, and unchanged rows per scenario.

===========================================================
"""

import pandas as pd
from pathlib import Path

# Path to folder containing all files
folder_path = r"C:\Users\bipas\Downloads\idea-data\idea" #Change to enter path of the folder containing the idea files (NOT the filename itself)
folder = Path(folder_path)

csv_files = list(folder.glob("*.csv"))

target_files = [f for f in csv_files if f.name.endswith("_results_general_IDEA_SK.csv")]
source_files = [f for f in csv_files if f.name.endswith("_output_summary_IDEA_SK.csv")]

source_dict = {}
for sf in source_files:
    scenario_name = sf.name.replace("_output_summary_IDEA_SK.csv", "")
    source_dict[scenario_name] = sf

for tf in target_files:
    scenario_name = tf.name.replace("_results_general_IDEA_SK.csv", "")
    if scenario_name not in source_dict:
        print(f"Skipping {tf.name}: no matching source file found")
        continue

    source_file = source_dict[scenario_name]

    print(f"\nProcessing scenario '{scenario_name}':")
    print(f"  Target file: {tf.name}")

    print(f"  Source file: {source_file.name}")

    target_df = pd.read_csv(tf)
    source_df = pd.read_csv(source_file)

    # Filter source
    source_filtered = source_df[
        source_df['variable'].str.startswith("Emissions|Electricity") &
        (source_df['region'] == "Saskatchewan.a")
    ]

    year_col = 'time' if 'time' in source_filtered.columns else 'year'

    source_totals = (
        source_filtered
        .groupby([year_col, 'scenario'], as_index=False)['value']
        .sum()
        .rename(columns={'value': 'new_total'})
    )
    source_totals['new_total'] = source_totals['new_total'] * 1_000_000  # MtCO₂ → tonnes

    source_lookup = {
        (float(row[year_col]), row['scenario']): row['new_total']
        for _, row in source_totals.iterrows()
    }

    updated_df = target_df.copy()
    updated_count = 0
    zeroed_count = 0

    for (year, scenario), group_df in updated_df.groupby(['year', 'scenario']):
        # Get only the matching emission rows
        relevant_rows_idx = [
            idx for idx in group_df.index
            if updated_df.at[idx, 'full_path'] == "CIMS.CAN.SK.Electricity" and
               updated_df.at[idx, 'parameter'] == "total_cumul_net_emissions"
        ]
        if not relevant_rows_idx:
            continue

        key = (float(year), scenario)
        if key in source_lookup:
            new_total = source_lookup[key]
            split_value = new_total / len(relevant_rows_idx)
            print(f"\nYear: {year}, Scenario: {scenario}")
            print(f"  Total from source: {new_total} → there are {len(relevant_rows_idx)} relevant rows")
            for idx in relevant_rows_idx:
                old_value = updated_df.at[idx, 'value_num']
                if updated_df.at[idx, 'context'] == "CO2":
                    updated_df.at[idx, 'value_num'] = new_total
                    print(f"    Row {idx} | context=CO2 | old={old_value} → new={new_total}")
                else:
                    updated_df.at[idx, 'value_num'] = 0
                    print(f"    Row {idx} | context={updated_df.at[idx,'context']} | old={old_value} → new=0")
                    zeroed_count += 1
            updated_count += 1
        else:
            print(f"\nYear: {year}, Scenario: {scenario}")
            print(f"  No matching source data found → Set value_num to 0")
            for idx in relevant_rows_idx:
                old_value = updated_df.at[idx, 'value_num']
                updated_df.at[idx, 'value_num'] = 0
                zeroed_count += 1
                print(f"    Row {idx} | parameter={updated_df.at[idx,'parameter']} "
                      f"| context={updated_df.at[idx,'context']} "
                      f"| full_path={updated_df.at[idx,'full_path']} "
                      f"| old={old_value} → new=0")


    output_file = tf.with_name(tf.stem + "_updated.csv")
    updated_df['model'] = updated_df['model'].replace("CIMS", "CIM2")
    updated_df.to_csv(output_file, index=False)

    unchanged_count = len(target_df) - (updated_count + zeroed_count)
    print(f"  Updated rows: {updated_count}")
    print(f"  Zeroed rows: {zeroed_count}")
    print(f"  Unchanged rows: {unchanged_count}")
    print(f"  Saved updated file to: {output_file.name}")

def update_cims_prices(folder: Path):
    """
    Processes all *_cims_prices.csv files in the folder.
    Replaces 'CIMS' with 'CIM2' in the 'model' column for all rows.
    Saves the updated file with the same filename (overwrite).
    """
    prices_files = list(folder.glob("*_cims_prices.csv"))
    if not prices_files:
        print("No *_cims_prices.csv files found.")
        return

    for pf in prices_files:
        df = pd.read_csv(pf)
        if 'model' in df.columns:
            count_before = (df['model'] == 'CIMS').sum()
            df['model'] = df['model'].replace("CIMS", "CIM2")
            count_after = (df['model'] == 'CIMS').sum()
            df.to_csv(pf, index=False)
            print(f"Processed {pf.name}: Replaced {count_before} occurrences of 'CIMS' → 'CIM2' (remaining {count_after})")
        else:
            print(f"Skipped {pf.name}: no 'model' column found.")


update_cims_prices(folder)
