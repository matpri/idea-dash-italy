import os
import pandas as pd
from openpyxl import load_workbook

from profiles.copper_output import utils
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
        if (df.model == 'macromodel').any():
            if df.variable.str.startswith("Histogram").any():
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
        df["variable"] = df["variable"].str.replace('_', ' ')
        df["variable"] = df["variable"].str.capitalize()
        gen_cap = df[df.variable.str.startswith("Histogram|")]
        gen_cap['value'] = gen_cap['value'].astype(float)

        gen_cap['type'] = gen_cap['variable'].apply(lambda x: x.split("|")[1])
        gen_cap['variable'] = gen_cap['variable'].apply(lambda x: '|'.join(x.split("|")[2:-1]))
        gen_cap["variable"] = gen_cap["variable"].str.capitalize()
        gen_cap["type"] = gen_cap["type"].str.capitalize()
        # gen_cap = gen_cap.groupby(['region', 'variable', 'time', 'scenario', 'unit', 'type'])['value'].apply(list).reset_index()
        gen_caps.append(gen_cap)

    full_net_new_cap = pd.concat(gen_caps)
    return full_net_new_cap



