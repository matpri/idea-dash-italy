import os
import pandas as pd
from openpyxl.reader.excel import load_workbook

from profiles.nextgrid_output import utils

def check(df):
    """
    Check if emissions in the 'variable' column contain specific prefixes.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefixes are found, False otherwise.
    """
    #print("Checking for net new cap in variable column")
    try:
        if (df.model == 'ECCC-NextGrid').any():
            if df.variable.str.startswith("Total generation capacity").any():
                return True
        return False
    except Exception as e:
        #print("net new cap  check", e)
        return False


def process_gencap(prov_df, canada_df, scenario_name):
    """
    Process generation capacity data.

    Parameters:
        prov_df (pd.DataFrame): Data for the provinces.
        canada_df (pd.DataFrame): Data for Canada.
        scenario_name (str): Name of the scenario.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    prov_df["region"] = prov_df["region"].apply(lambda x: x.split(".")[0])
    prov_df['region'] = prov_df['region'].map(utils.province_short).fillna(prov_df['region'])
    df = pd.concat([prov_df, canada_df])

    # make value for any variable that contains retire negative
    df.loc[df['variable'].str.contains("retire"), 'value'] = df.loc[df['variable'].str.contains("retire"), 'value'] * -1
    df = df.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
    df['value'] = df['value'].div(1000)
    df['scenario'] = scenario_name
    return df

def process_extant(gen_cap, path, scenario_name):
    extant = pd.read_csv(path)
    extant['region'] = extant['ABA'].str.split('.').str[0]
    extant['variable'] = extant['ABA'].str.split('.').str[2]

    # drop ABA column
    extant = extant.drop(columns=['ABA'])

    extant = pd.melt(extant, id_vars=['region', 'variable'], var_name='time', value_name='value')
    extant = extant.groupby(['region', 'variable', 'time']).sum().reset_index()

    # add region Canada which is sum of all regions
    extant_canada = extant.groupby(['variable', 'time']).sum().reset_index()
    extant_canada['region'] = 'CAN'

    # append to extant
    extant = pd.concat([extant, extant_canada], ignore_index=True)
    # apply utils.province_short
    extant['region'] = extant['region'].map(utils.province_short).fillna(extant['region'])
    # only keep time 2021
    extant = extant[extant['time'] == '2021']
    # aggregate
    extant = extant.groupby(['region', 'variable', 'time']).sum().reset_index()

    extant['value'] = extant['value'].div(1000)

    extant['scenario'] = scenario_name
    extant['time'] = extant['time'].astype(int)

    return pd.concat([gen_cap, extant], ignore_index=True)

def process_net_new_cap(gen_cap):
    """
    Process net new capacity data.

    Parameters:
        gen_cap (pd.DataFrame): Generation capacity data.

    Returns:
        pd.DataFrame: Processed net new capacity DataFrame.
    """
    diff_df = pd.DataFrame(columns=['variable', 'region', 'scenario', 'time', 'value'])

    # Iterate over each unique combination of variable, region, and scenario
    for name, group in gen_cap.groupby(['variable', 'region', 'scenario']):
        group = group.sort_values(by='time')
        group['value'] = group['value'].diff().fillna(0)  # Calculate the difference over time
        diff_df = pd.concat([diff_df, group])

    # Reset the index of the resulting DataFrame
    diff_df.reset_index(drop=True, inplace=True)
    return diff_df

def process(dbs: dict):
    """
    Process generation capacity and derive net new capacity.

    Parameters:
        dbs (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    net_new_caps = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        prov_df = df[df.variable.str.startswith("Total generation capacity|")]
        prov_df['value'] = prov_df['value'].astype(float)
        canada_df = prov_df.groupby(['time', 'scenario', 'variable']).sum(numeric_only=True).reset_index()
        canada_df['region'] = 'CAN'
        prov_df['variable'] = prov_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        canada_df['variable'] = canada_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        gen_cap = process_gencap(prov_df, canada_df, scenario_name)

        net_new_cap = process_net_new_cap(gen_cap)

        net_new_caps.append(net_new_cap)

    full_net_new_cap = pd.concat(net_new_caps)
    full_net_new_cap['time'] = full_net_new_cap['time'].astype(int)

    value_sum_per_year = full_net_new_cap.groupby('time')['value'].sum()
    years_with_non_zero_values = value_sum_per_year[value_sum_per_year != 0].index
    full_net_new_cap = full_net_new_cap[full_net_new_cap['time'].isin(years_with_non_zero_values)]
    return full_net_new_cap