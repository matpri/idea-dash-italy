import pandas as pd
import os

from profiles.copper_output import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for emissions in variable column")
    try:
        if (df.model == 'copper_input').any():
            if df.variable.str.startswith("US Demand").any():
                return True
        return False
    except Exception as e:
        print("Emission check", e)
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
    # Group by period and technology and sum the values
    canadian_total = df.groupby(["time", "variable"]).sum(numeric_only=True).reset_index()
    canadian_total["region"] = "CAN"
    return canadian_total


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df = df[df.variable.str.startswith("US Demand")]
        df['region'] = df['region'].str.split('.').str[0]
        df = df.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df
