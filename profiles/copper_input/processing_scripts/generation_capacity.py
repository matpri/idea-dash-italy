import os
import pandas as pd
import geopandas as gpd
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
    #print("Checking for gen cap in variable column")
    try:
        if (df.model == 'copper_input').any():
            if df.variable.str.startswith("Capacity").any() or df.variable.str.startswith("Merra|").any():
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
    gen_caps = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        dfs = []
        if df.variable.str.startswith("Capacity|").any():
            gen_df = db.copy()
            prov_df = df[df.variable.str.startswith("Capacity|")]
            prov_df['value'] = prov_df['value'].astype(float)
            canada_df = prov_df.groupby(['time', 'scenario', 'variable']).sum(numeric_only=True).reset_index()
            canada_df['region'] = 'CAN'
            prov_df['variable'] = prov_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
            canada_df['variable'] = canada_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
            gen_cap = process_gencap(prov_df, canada_df, scenario_name)
            dfs.append(gen_cap)
        if df.variable.str.startswith("Merra|").any():
            merra_df = db.copy()
            prov_df = merra_df[df.variable.str.startswith("Merra|")]
            prov_df['variable'] = prov_df['variable'].str.split('|').str[1]
            prov_df['value'] = prov_df['value'].astype(float)

            merra_cells = gpd.read_file('profiles/copper_input/visualization_scripts/utils/merra2_cells.geojson')

            prov_df = prov_df.merge(merra_cells, left_on='region', right_on='grid_cell', how='left')

            prov_df = prov_df[['time', 'balancing_area', 'value', 'variable']]
            prov_df = prov_df.rename(
                columns={'time': 'time', 'balancing_area': 'region', 'value': 'value', 'variable': 'variable'})
            prov_df[['region', 'aba']] = prov_df['region'].str.split('.', expand=True)
            prov_df['region'] = prov_df['region'].map(utils.province_short) + '.' + prov_df['aba']
            prov_df = prov_df.drop(columns='aba')
            dfs.append(prov_df)

        gen_caps.append(pd.concat(dfs))

    full_net_new_cap = pd.concat(gen_caps)
    full_net_new_cap['time'] = full_net_new_cap['time'].astype(int)

    return full_net_new_cap



