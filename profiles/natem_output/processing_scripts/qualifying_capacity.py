import os
import pandas as pd

from profiles.natem_output import utils

def check(df):
    """
    Check if generation capacity is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefixes are found, False otherwise.
    """
    #print("Checking for gen cap in variable column")
    try:
        if (df.model == 'NATEM_Canad').any():
            if df.variable.str.startswith("Qualifying capacity|").any():
                return True
        return False
    except Exception as e:
        print("gen cap  check", e)
        return False



def process_qual_cap(qual_cap, scenario_name):
    """
    Process qualifying capacity data.

    Parameters:
        qual_cap (pd.DataFrame): Data .
        scenario_name (str): Name of the scenario.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    qual_cap["region"] = qual_cap["region"].apply(lambda x: x.split(".")[0])
    qual_cap['region'] = qual_cap['region'].map(utils.province_short).fillna(qual_cap['region'])
    qual_cap['region'] = qual_cap['region'].apply(lambda x: x[:2].upper())

    can_qual_cap = qual_cap.groupby(['variable', 'region', 'time']).sum().reset_index()
    can_qual_cap['region'] = 'CAN'
    df = pd.concat([qual_cap, can_qual_cap])



    df['scenario'] = scenario_name
    summer_df = df.copy()
    summer_df['season'] = 'summer'

    winter_df = df.copy()
    winter_df['season'] = 'winter'

    df = pd.concat([summer_df, winter_df])


    # df = df[df['value'] != 0]
    df = df[~df['variable'].str.contains('retire')]
    df['value'] = df.value.div(1000)
    return df

def process(dbs: dict):
    """
    Process qualifying capacity and derive a DataFrame.

    Parameters:
        dbs (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    gen_caps = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        df = df[df.variable.str.startswith("Qualifying capacity|")]

        df['variable'] = df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        gen_cap = process_qual_cap(df, scenario_name)

        gen_caps.append(gen_cap)


    full_data = pd.concat(gen_caps)

    full_data['time'] = full_data['time'].astype(int)
    return full_data


