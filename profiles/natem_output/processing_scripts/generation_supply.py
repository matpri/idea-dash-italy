import glob
import os

import pandas as pd

from profiles.natem_output import utils


def check(df):
    """
    Check if emissions in the 'variable' column contain strings like 'transmission|', '*out', and 'supply|'.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified strings are found, False otherwise.
    """
    #print("Checking for dispatch, *out and transmission in variable column")
    try:
        if (df.model == 'NATEM_Canad').any():
            classes = df["variable"].apply(lambda x: x.split("|")[0])
            if (classes == 'Dispatch').any() or (classes == 'Transmission flow').any():
                return True
        return False
    except Exception as e:
        print("dispatch check", e)
        return False


def aggregate_db(db, scenario):
    """
    Aggregate and format data from the 'db' DataFrame based on specific conditions.

    Parameters:
        db (pd.DataFrame): DataFrame to aggregate.
        scenario (str): Name of the scenario.

    Returns:
        pd.DataFrame: Aggregated and formatted DataFrame.
    """
    # safely remove model and unit column if they exist
    db = db.drop(columns=['model', 'unit'], errors='ignore')

    classes = db["variable"].apply(lambda x: x.split("|")[0])

    db["region"] = db.region.apply(lambda x: x.split(".")[0])
    supply_df = db[classes == 'Dispatch']
    supply_df["variable"] = supply_df["variable"].apply(lambda x: '|'.join(x.split("|")[1:]))

    supply_df['time'] = pd.to_datetime(supply_df['time'])

    # all times - 1 hour delta
    supply_df['period'] = supply_df['time'].dt.year
    sub_supply = supply_df[supply_df['period'] == supply_df['period'].min()]
    unique_dates = sub_supply['time'].dt.date.unique()

    # rename region entries based on utils.province_short
    supply_df['region'] = supply_df['region'].map(utils.province_short).fillna(supply_df['region'])
    # aggregate the dim_name based on the tech_agg_COPPER dictionary
    # change value from MWh to TWh
    supply_df['value'] = supply_df['value'] / 1000000
    # expand value to an entire year by multiplying by 365/12
    supply_df['value'] = supply_df['value'] * 365 / len(unique_dates)
    # make period an int
    supply_df['period'] = supply_df['period'].astype(int)
    supply_df.drop(columns=['time'], inplace=True)

    transmission_df = db[classes == 'Transmission flow']
    transmission_df["variable"] = transmission_df["variable"].apply(lambda x: '|'.join(x.split("|")[1:]))
    # replace to with ''
    transmission_df['variable'] = transmission_df['variable'].str.replace('to ', '')
    transmission_df["variable"] = transmission_df.variable.apply(lambda x: x.split(".")[0])

    # time to datetime object
    transmission_df['time'] = pd.to_datetime(transmission_df['time'])
    transmission_df['time'] = transmission_df['time'] - pd.Timedelta(hours=1)
    transmission_df['period'] = transmission_df['time'].dt.year
    # make period an int
    transmission_df['period'] = transmission_df['period'].astype(int)

    transmission_df.drop(columns=['time'], inplace=True)

    # drop all the 0 values
    # transmission_df = transmission_df[transmission_df.value != 0]
    transmission_df['value'] = transmission_df['value'] * -1

    # aggregate df values by region, variable, time, hour
    transmission_df = transmission_df.groupby(["region", "variable", "period"]).sum().reset_index()
    # rename from and variable based on utils.province_short
    transmission_df["region"] = transmission_df.region.map(utils.province_short).fillna(transmission_df['region'])
    transmission_df["variable"] = transmission_df.variable.map(utils.province_short).fillna(transmission_df['variable'])

    # drop rows where region == variable
    transmission_df = transmission_df[transmission_df.region != transmission_df.variable]

    # create a dataframe where the region and variable are swapped and the value is -1* the value
    transmission_df_swap = transmission_df.copy()
    transmission_df_swap["region"] = transmission_df["variable"]
    transmission_df_swap["variable"] = transmission_df["region"]
    transmission_df_swap["value"] = -1 * transmission_df["value"]

    transmission_df = pd.concat([transmission_df, transmission_df_swap], ignore_index=True)
    transmission_df["region"] = transmission_df.region.apply(lambda x: x.split(".")[0])
    # rename region entries based on utils.province_short
    transmission_df['region'] = transmission_df['region'].map(utils.province_short).fillna(transmission_df['region'])
    dim_names = []
    for index, row in transmission_df.iterrows():
        if row['value'] < 0:
            dim_names.append(f"Exports to {row['variable']}")
        else:
            dim_names.append(f"Imports from {row['variable']}")

    transmission_df['end_node'] = transmission_df['variable']
    transmission_df['variable'] = dim_names
    transmission_df = transmission_df.groupby(['period', 'region', 'variable']).sum().reset_index()
    # change value from MWh to TWh
    transmission_df['value'] = transmission_df['value'] / 1000000
    # expand value to an entire year by multiplying by 365/12
    transmission_df['value'] = transmission_df['value'] * 365 / len(unique_dates)


    # only keep the periods that are in the supply_df
    transmission_df = transmission_df[transmission_df.period.isin(supply_df.period.unique())]

    #only keep the regions that are in the supply_df
    transmission_df = transmission_df[transmission_df.region.isin(supply_df.region.unique())]



    df = pd.concat([supply_df, transmission_df])
    # df = df[df.value != 0]
    df = df.groupby(['period', 'region', 'variable']).sum().reset_index()

    df['scenario'] = scenario
    can_df = df.groupby(['variable', 'period', 'scenario','end_node']).sum(numeric_only=True).reset_index()
    # can_df remove all variables that start with Import or Export
    can_df = can_df[~can_df.variable.str.startswith('Imports from')]
    can_df = can_df[~can_df.variable.str.startswith('Exports to')]
    can_df['region'] = 'CAN'
    df = pd.concat([df, can_df], ignore_index=True)

    # sort by dim_name and period
    df = df.sort_values(by=['variable', 'period'])

    # remove time column and rename period column
    df = df.rename(columns={"period": "time"})

    # make time an int
    df.time = df.time.astype(int)
    return df

def process(selected):
    """
    Process the selected scenarios from the 'selected' dictionary.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario, db in selected.items():
        df_processed = aggregate_db(db.copy(), scenario)

        dfs.append(df_processed)

    full_data = pd.concat(dfs)

    full_data['time'] = full_data['time'].astype(int)
    return full_data
