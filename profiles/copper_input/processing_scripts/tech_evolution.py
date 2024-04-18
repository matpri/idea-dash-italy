import os
import pandas as pd
from openpyxl import load_workbook

from profiles.copper_input import utils
def check(df):
    """
    Check if emissions in the 'variable' column contain strings like 'Results_summary_ABA_generation_mix|' or 'Results_summary_Canada_generation_mix|'.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified strings are found, False otherwise.
    """
    print("Checking for gen cap in variable column")
    try:
        if (df.model == 'copper_input').any():
            if df.variable.str.startswith("Technology Evolution").any():
                return True
        return False
    except Exception as e:
        print("gen cap  check", e)
        return False

def process(dbs: dict):
    """
    Process generation capacity data from multiple scenarios.

    Parameters:
        dbs (dict): Dictionary containing DataFrames for different scenarios.

    Returns:
        pd.DataFrame: Processed generation capacity data.
    """
    gen_caps = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        prov_df = df[df.variable.str.startswith("Technology Evolution")]
        prov_df['value'] = prov_df['value'].astype(float)

        gen_caps.append(prov_df)

    full_net_new_cap = pd.concat(gen_caps)
    full_net_new_cap['time'] = full_net_new_cap['time'].astype(int)

    return full_net_new_cap



