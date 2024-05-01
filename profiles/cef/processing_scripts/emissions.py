import pandas as pd
import os

from openpyxl.reader.excel import load_workbook

from profiles.cef import utils
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
        if (df.model == 'cef').any():
            if df.variable.str.startswith("greenhouse_gas_emissions|").any():
                return df[df.variable.str.startswith("greenhouse_gas_emissions|")]['value'].sum() != 0
        return False
    except Exception as e:
        print("cost check", e)
        return False

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
        df = db[db.variable.str.startswith("greenhouse_gas_emissions|")].copy()
        df.columns = df.columns.str.lower()
        df['variable'] = df["variable"].apply(lambda x: x.split("|")[1])
        df = df.rename(columns={'year': 'time'})
        df['region'] = df.region.map(utils.province_short).fillna(df.region)
        df = df[df['variable'] == 'Electricity']
        # rename canada to can
        df['region'] = 'CAN'
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df
