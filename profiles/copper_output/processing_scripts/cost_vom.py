import pandas as pd
import os

from profiles.copper_output import utils


def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for cost in variable column")
    try:
        if (df.model == 'copper').any():
            if df.variable.str.startswith("Variable O&M Costs|").any():
                return df[df.variable.str.startswith("Variable O&M Costs|")]['value'].sum() != 0
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
    df = df.groupby(['region', 'variable', 'time', 'scenario', 'unit']).sum(numeric_only=True).reset_index()
    return df


def calculate_vom(vom_df):
    """
    Calculates the variable operating and maintenance (VOM) cost data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated VOM cost data.

    """
    # vom_df = df[df['variable'].isin(utils.vom_names)].copy()
    # vom_df['variable'] = vom_df['variable'].map(utils.cost_tech).fillna(vom_df['variable'])
    vom_df = vom_df.groupby(["variable", "region", "time", "scenario", 'unit']).sum(numeric_only=False).reset_index()

    # Aggregate data over all regions by variable, time, and scenario and sum the values
    can_vom_df = vom_df.groupby(["variable", "time", "scenario", 'unit'], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "Can"
    can_vom_df = can_vom_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    vom_df = pd.concat([vom_df, can_vom_df], ignore_index=True)

    return vom_df


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
        df = df[df.variable.str.startswith("Variable O&M Costs|")]
        df['variable'] = df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        formatted_df = format_df(df)
        formatted_df = calculate_vom(formatted_df)
        formatted_df['scenario'] = scenario_name
        dfs.append(formatted_df)
    full_df = pd.concat(dfs)
    full_df['unit'] = '$ Billions'
    full_df['value'] = full_df['value'].div(1e9)
    full_df['region'] = full_df['region'].apply(lambda x: x.split('.')[0])
    return full_df
