import pandas as pd
import os

from profiles.recap import utils


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
        if (df.model == 'CIM2').any():
            if (df.parameter.str.contains('emissions')).any():
                return True
        return False
    except Exception as e:
        print("ghg check", e)
        return False

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        df = df[df['parameter'].str.contains('emissions')]
        # remove where region is CAN
        df = df[~df['region'].str.contains('CAN')]
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    full_df['value_num'] = full_df['value_num'].astype(float)
    return full_df
