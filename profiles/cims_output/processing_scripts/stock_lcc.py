import pandas as pd
import os

from profiles.cims_output import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for emissions in variable column")
    try:
        if (df.model == 'CIMS').any():
            if (df.parameter.str.contains('stock')).any():
                return True
        return False
    except Exception as e:
        print("Emission check", e)
        return False

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df
