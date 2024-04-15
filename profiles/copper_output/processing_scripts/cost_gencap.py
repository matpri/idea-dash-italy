import pandas as pd
import os

from openpyxl.reader.excel import load_workbook

from profiles.copper_output import utils

def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for cost in variable column")
    try:
        if df.variable.str.startswith("Capital Costs|").any():
            return df[df.variable.str.startswith("Capital Costs|")]['value'].sum() != 0
        return False
    except Exception as e:
        print("cost check", e)
        return False

def format_df(df):
    """
    Extracts province, year, and other relevant information from column names in the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Formatted data with extracted information.
    """
    df['region'] = df['region'].map(utils.province_short).fillna(df['region'])
    df = df.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
    return df

def calc_canadian(df):
    """
    Calculates the Canadian total for each year and technology.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Formatted data with extracted information.
    """
    # Group by time and technology and sum the values
    canadian_total = df.groupby(["time", "variable"]).sum(numeric_only=True).reset_index()
    canadian_total["region"] = "CAN"
    return canadian_total

def calculate_generation_capacity(gen_cap_df):
    """
    Calculates the generation capacity data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated generation capacity data.

    """
    # Extract generation capacity data from df
    # gen_cap_df = df[df['variable'].isin(utils.gen_cap_names)].copy()
    # Rename entries based on gen_cap_names_dict
    # gen_cap_df['variable'] = gen_cap_df['variable'].map(utils.cost_tech).fillna(gen_cap_df['variable'])
    gen_cap_df = gen_cap_df.groupby(["variable", "region", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Compute Canadian total over all regions
    can_gen_cap_df = gen_cap_df.groupby(["variable", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "CAN"
    can_gen_cap_df = can_gen_cap_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    gen_cap_df = pd.concat([gen_cap_df, can_gen_cap_df], ignore_index=True)

    return gen_cap_df

def process(data):
    """
    Process emission data from multiple scenarios based on the 'folders' dictionary.

    Parameters:
        folders (dict): Dictionary containing scenario names as keys and folder paths as values.
        target_dir (str): Target directory.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario_name, db in data.items():
        df = db.copy()
        df = df[df.variable.str.startswith("Capital Costs|")]
        df['variable'] = df['variable'].apply(lambda x: x.split("|")[1])
        formatted_df = format_df(df)
        formatted_df = calculate_generation_capacity(formatted_df)
        formatted_df['scenario'] = scenario_name
        dfs.append(formatted_df)
    full_df = pd.concat(dfs)
    full_df['unit'] = '$ Billions'
    full_df['value'] = full_df['value'].div(1e9)
    return full_df
