import glob
import os

import pandas as pd

from profiles.cef import utils


def check(df):
    """
    Check if emissions in the 'variable' column contain strings like 'transmission|', '*out', and 'supply|'.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified strings are found, False otherwise.
    """
    #print("Checking for dispatch, *out and transmission in variable column")
    try:
        if (df.model == 'cef').any():
            classes = df["variable"].apply(lambda x: x.split("|")[0])
            if (classes == 'electricity_generation').any():
                return True
        return False
    except Exception as e:
        print("dispatch check", e)
        return False


def process(selected):
    """
    Process the selected scenarios from the 'selected' dictionary.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario, db in selected.items():
        df = db[db.variable.str.startswith("electricity_generation|")].copy()
        df.columns = df.columns.str.lower()
        df['variable'] = df["variable"].apply(lambda x: x.split("|")[1])
        df = df.rename(columns={'year': 'time'})
        df['unit'] = 'TWh'
        df['value'] = df['value'].div(1e3)

        df['region'] = df.region.map(utils.province_short).fillna(df.region)
        # rename canada to can
        df['region'] = df['region'].replace({'Canada': 'CAN'})
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df
