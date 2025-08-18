import pandas as pd
from pathlib import Path

def convert_credits_to_iamc(df, unit="$"):
    """
    Convert credit balances CSV to IAMC format and return the dataframe.
    """
    iamc_rows = []

    for var_col, var_name in [
        ("credit_supply", "Credit Supply"),
        ("credit_demand", "Credit Demand"),
        ("net_balance", "Net Balance"),
    ]:
        temp = df.copy()
        temp[var_col] = temp[var_col].fillna(0)
        temp["variable"] = temp["sector"].apply(lambda s: f"{var_name}|{s}")
        temp = temp.rename(columns={"year": "time", var_col: "value"})
        temp["model"] = "CIM2"
        temp["region"] = "SK"
        temp = temp[["model", "scenario", "region", "time", "variable", "value"]]
        temp["unit"] = unit
        temp["variable"] = "Credits|" + temp["variable"]
        # (Might need to be changed) Divide all values by 100 to maitain order of magnitude
        # temp["value"] = temp["value"] / 100

        # Making supply negative to match COPPER format
        mask = temp["variable"].str.contains("Credit Supply", case=False, na=False)
        temp.loc[mask, "value"] = -temp.loc[mask, "value"]
        iamc_rows.append(temp)

    iamc_df = pd.concat(iamc_rows, ignore_index=True)
    return iamc_df

def summarize_carbon_credits_ignore_model(df, iamc_df, unit="$"):
    """
    Summarize Carbon Credit and Carbon Costs for Saskatchewan, and merge with IAMC df.
    Overwrite matching rows and add new rows if necessary, ignoring 'model' differences.
    """
    df = df[df["region"] == "Saskatchewan.a"]

    credit_vars = df[df["variable"].str.startswith("Carbon Credit")]
    cost_vars = df[df["variable"].str.startswith("Carbon Costs")]

    summarized_rows = []

    # Summarize credit supply
    credit_summary = (
        credit_vars.groupby(["region", "scenario", "time"], as_index=False)["value"].sum()
    )
    credit_summary["variable"] = "Credits|Credit Supply|Electricity"
    credit_summary["unit"] = unit
    summarized_rows.append(credit_summary)

    # Summarize credit demand / costs
    cost_summary = (
        cost_vars.groupby(["region", "scenario", "time"], as_index=False)["value"].sum()
    )
    cost_summary["variable"] = "Credits|Credit Demand|Electricity"
    cost_summary["unit"] = unit
    summarized_rows.append(cost_summary)

    summary_df = pd.concat(summarized_rows, ignore_index=True)
    summary_df["region"] = "SK"
    summary_df["model"] = "CIM2"

    iamc_columns = ["model", "scenario", "region", "time", "variable", "value", "unit"]
    summary_df = summary_df[iamc_columns]

    
    demand_df = summary_df[summary_df["variable"] == "Credits|Credit Demand|Electricity"]
    supply_df = summary_df[summary_df["variable"] == "Credits|Credit Supply|Electricity"]

    merge_keys = ["model", "scenario", "region", "time", "unit"]
    merged = pd.merge(
        demand_df, 
        supply_df, 
        on=merge_keys, 
        how="outer", 
        suffixes=("_demand", "_supply")
    )

    merged["value_demand"] = merged["value_demand"].fillna(0)
    merged["value_supply"] = merged["value_supply"].fillna(0)

    merged["value"] = merged["value_demand"] + merged["value_supply"]

    net_balance_df = merged[merge_keys + ["value"]].copy()
    net_balance_df["variable"] = "Credits|Net Balance|Electricity"

    summary_df = pd.concat([summary_df, net_balance_df], ignore_index=True)

    summary_df = summary_df.sort_values(by=["region", "time", "variable"]).reset_index(drop=True)

    updated_count = 0
    added_count = 0

    for _, row in summary_df.iterrows():
        mask = (
            (iamc_df["scenario"] == row["scenario"]) &
            (iamc_df["region"] == row["region"]) &
            (iamc_df["time"] == row["time"]) &
            (iamc_df["variable"] == row["variable"])
        )
        if mask.any():
            old_value = iamc_df.loc[mask, "value"].values[0]
            iamc_df.loc[mask, "value"] = row["value"]
            updated_count += 1
            print(f"Updated row: scenario={row['scenario']}, region={row['region']}, "
                  f"time={row['time']}, variable={row['variable']}, "
                  f"old_value={old_value}, new_value={row['value']}")
        else:
            iamc_df = pd.concat([iamc_df, pd.DataFrame([row])], ignore_index=True)
            added_count += 1
            print(f"Added new row: scenario={row['scenario']}, region={row['region']}, "
                  f"time={row['time']}, variable={row['variable']}, value={row['value']}")

    print(f"\nSummary for IAMC update: {updated_count} rows updated, {added_count} rows added.\n")
    return iamc_df

folder_path = r"C:\Users\bipas\Downloads\idea-data\final" #Change to enter path of the folder containing the idea files (NOT the filename itself)
folder = Path(folder_path)

csv_files = list(folder.glob("*.csv"))

target_files = [f for f in csv_files if f.name.endswith("_credit_balance.csv")]
source_files = [f for f in csv_files if f.name.endswith("_output_summary_IDEA_SK.csv")]

source_dict = {sf.name.replace("_output_summary_IDEA_SK.csv", ""): sf for sf in source_files}

for tf in target_files:
    scenario_name = tf.name.replace("_credit_balance.csv", "")
    if scenario_name in source_dict:
        source_file = source_dict[scenario_name]
    else:
        # --- Fallback: substring match ---
        possible_matches = [sf for key, sf in source_dict.items() if scenario_name in key]

        if not possible_matches:
            print(f"Skipping {tf.name}: no matching source file found (even by substring).")
            continue
        elif len(possible_matches) > 1:
            print(f"Warning: Multiple source files match target '{tf.name}' by substring:")
            for pm in possible_matches:
                print(f"   - {pm.name}")
            print("Skipping due to ambiguity.")
            continue
        else:
            source_file = possible_matches[0]
            print(f"Note: Using substring match for '{tf.name}' → matched with '{source_file.name}'")

    # --- Load files ---
    print(f"\nProcessing scenario '{scenario_name}':")
    print(f"  Target file: {tf.name}")
    print(f"  Source file: {source_file.name}")
    target_df = pd.read_csv(tf)
    source_df = pd.read_csv(source_file)

    iamc_df = convert_credits_to_iamc(target_df, unit="$")
    final_df = summarize_carbon_credits_ignore_model(source_df, iamc_df, unit="$")
    final_df['model'] = "CIM2"
    output_file = tf.with_name(tf.stem + "_updated.csv")
    final_df.to_csv(output_file, index=False)
    print(f"  Saved updated file to: {output_file.name}")
    try:
        # tf.unlink()
        print(f"  Deleted original file: {tf.name}")
    except Exception as e:
        print(f"  Could not delete {tf.name}: {e}")