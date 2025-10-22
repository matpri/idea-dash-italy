import os
import pandas as pd
from openpyxl import load_workbook

from profiles.natem_output import utils
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
        if (df.model == 'NATEM_Canada').any():
            if df.variable.str.startswith("Total generation capacity").any():
                return True
        return False
    except Exception as e:
        print("gen cap  check", e)
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
    gen_caps = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        prov_df = df[df.variable.str.startswith("Total generation capacity|")]
        prov_df['value'] = prov_df['value'].astype(float) / 1000  # Convert from MW to GW
        # if 'CAN' not in prov_df['region'].values:
        #     canada_df = prov_df.groupby(['time', 'scenario', 'variable']).sum(numeric_only=True).reset_index()
        #     canada_df['region'] = 'CAN'
        #     canada_df['variable'] = canada_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        prov_df['variable'] = prov_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        prov_df = prov_df.groupby(['region', 'time', 'scenario', 'variable']).sum(numeric_only=True).reset_index()
        prov_df['scenario'] = scenario_name

        # if 'CAN' not in prov_df['region'].values:
        #     gen_cap = process_gencap(prov_df, canada_df, scenario_name)
        # else:
        #     gen_cap = process_gencap(prov_df, pd.DataFrame(), scenario_name)

        gen_caps.append(prov_df)

    full_net_new_cap = pd.concat(gen_caps)
    full_net_new_cap['time'] = full_net_new_cap['time'].astype(int)

    return full_net_new_cap



