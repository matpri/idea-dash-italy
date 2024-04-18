import os
import pandas as pd

from profiles.copper_output import utils

def check(df):
    """
    Check if generation capacity is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefixes are found, False otherwise.
    """
    print("Checking for gen cap in variable column")
    try:
        if (df.model == 'copper').any():
            if df.variable.str.startswith("Qualifying_capacity_summer|").any() or df.variable.str.startswith("Qualifying_capacity_winter|").any():
                return True
        return False
    except Exception as e:
        print("gen cap  check", e)
        return False



def process_qual_cap(winter_df, summer_df, scenario_name):
    """
    Process qualifying capacity data.

    Parameters:
        winter_df (pd.DataFrame): Data for winter.
        summer_df (pd.DataFrame): Data for summer.
        scenario_name (str): Name of the scenario.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    winter_df["region"] = winter_df["region"].apply(lambda x: x.split(".")[0])
    winter_df['region'] = winter_df['region'].map(utils.province_short).fillna(winter_df['region'])
    winter_df['region'] = winter_df['region'].apply(lambda x: x[:2].upper())

    can_winter_df = winter_df.groupby(['variable', 'region', 'time']).sum().reset_index()
    can_winter_df['region'] = 'CAN'
    winter_df = pd.concat([winter_df, can_winter_df])

    summer_df["region"] = summer_df["region"].apply(lambda x: x.split(".")[0])
    summer_df['region'] = summer_df['region'].map(utils.province_short).fillna(summer_df['region'])
    summer_df['region'] = summer_df['region'].apply(lambda x: x[:2].upper())

    can_summer_df = summer_df.groupby(['variable', 'region', 'time']).sum().reset_index()
    can_summer_df['region'] = 'CAN'
    summer_df = pd.concat([summer_df, can_summer_df])

    winter_df['scenario'] = scenario_name
    winter_df['season'] = 'winter'
    summer_df['scenario'] = scenario_name
    summer_df['season'] = 'summer'

    df = pd.concat([winter_df, summer_df])

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
        winter_df = df[df.variable.str.startswith("Qualifying_capacity_winter|")]
        summer_df = df[df.variable.str.startswith("Qualifying_capacity_summer|")]

        winter_df['variable'] = winter_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        summer_df['variable'] = summer_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        gen_cap = process_qual_cap(winter_df, summer_df, scenario_name)

        gen_caps.append(gen_cap)


    full_data = pd.concat(gen_caps)

    full_data['time'] = full_data['time'].astype(int)
    return full_data


