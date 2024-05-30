import os
import pandas as pd
from openpyxl import load_workbook

from profiles.cef import utils
def check(df):
    """
    Check if emissions in the 'variable' column contain strings like 'Results_summary_ABA_generation_mix|' or 'Results_summary_Canada_generation_mix|'.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified strings are found, False otherwise.
    """
    #print("Checking for gen cap in variable column")
    try:
        if (df.model == 'cef').any():
            if df.variable.str.startswith("electricity_capacity").any():
                return True
        return False
    except Exception as e:
        #print("gen cap  check", e)
        return False

def process_gencap(prov_df, canada_df, scenario_name):
    """
    Process generation capacity data.

    Parameters:
        prov_df (pd.DataFrame): DataFrame containing province-specific generation capacity data.
        canada_df (pd.DataFrame): DataFrame containing Canada-wide generation capacity data.
        scenario_name (str): Name of the scenario.

    Returns:
        pd.DataFrame: Processed generation capacity data.
    """
    prov_df["region"] = prov_df["region"].apply(lambda x: x.split(".")[0])
    prov_df['region'] = prov_df['region'].map(utils.province_short).fillna(prov_df['region'])

    df = pd.concat([prov_df, canada_df])
    # remove variables that contain retire
    df = df[~df['variable'].str.contains("retire")]
    df['value'] = df['value'].div(1000)
    df = df.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
    df['scenario'] = scenario_name
    return df

def process(dbs: dict):
    """
    Process generation capacity data from multiple scenarios.

    Parameters:
        dbs (dict): Dictionary containing DataFrames for different scenarios.

    Returns:
        pd.DataFrame: Processed generation capacity data.
    """
    dfs = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        df = db[db.variable.str.startswith("electricity_capacity|")].copy()
        df.columns = df.columns.str.lower()
        df['variable'] = df["variable"].apply(lambda x: x.split("|")[1])
        df = df.rename(columns={'year': 'time'})
        df['unit'] = 'GW'
        df['value'] = df['value'].div(1000)
        df['region'] = df.region.map(utils.province_short).fillna(df.region)
        df = df[~df['variable'].str.contains("Total")]
        # rename canada to can
        df['region'] = df['region'].replace({'Canada': 'CAN'})
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df



