import glob
import os

import pandas as pd

from profiles.pithos_output import utils


def check(df):
    """
    Check if 'supply', 'transmission', and '*out' are present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefixes are found, False otherwise.
    """
    # check if emissions in variable column which has strings like transmission|AB -> BC, emissions|coal etc.
    print("Checking for dispatch, *out and transmission in variable column")
    try:
        if (df.model == 'ESMIA-PITHOS').any():
            if df.variable.str.startswith("Generation|").any() or df.variable.str.startswith(
                    "Flow|").any() or df.variable.str.startswith("Storage Out|").any() or df.variable.str.startswith("Storage In|").any():
                return True
        return False
    except Exception as e:
        print("dispatch check", e)
        return False

def aggregate_db(db, scenario):
    """
    Aggregate data from a DataFrame.

    Parameters:
        db (pd.DataFrame): Input DataFrame.
        scenario (str): Scenario name.

    Returns:
        pd.DataFrame: Aggregated DataFrame.
    """
    db.drop(columns=['model', "unit"], inplace=True, errors='ignore')

    classes = db["variable"].apply(lambda x: x.split("|")[0])

    db["region"] = db.region.apply(lambda x: x.split(".")[0])
    supply_df = db[classes == 'Generation']
    supply_df["variable"] = supply_df["variable"].apply(lambda x: '|'.join(x.split("|")[1:]))

    transmission_df = db[classes == 'Flow']
    transmission_df["variable"] = transmission_df["variable"].apply(lambda x: '|'.join(x.split("|")[1:]))
    transmission_df["variable"] = transmission_df.variable.apply(lambda x: x.split(".")[0])
    # aggregate df values by region, variable, time, hour
    transmission_df = transmission_df.groupby(["region", "variable", "time"]).sum().reset_index()
    # rename from and variable based on utils.province_short
    transmission_df["region"] = transmission_df.region.map(utils.province_short).fillna(transmission_df['region'])
    transmission_df["variable"] = transmission_df.variable.map(utils.province_short).fillna(transmission_df['variable'])

    # for every export create a new row with the region value being the Region in the dimname (export$region) and the variable being the region value and the value column being -1* the value column
    imports = []
    exports = []
    for index, row in transmission_df.iterrows():
        #
        exports.append([row["region"], row["time"], row["value"], "Exports"])
        imports.append([row["variable"], row["time"], row["value"], "Imports"])

    # create a new dataframe with the exports and imports using the same column names as the df dataframe with the additional column variable at the end
    exports = pd.DataFrame(exports, columns=["region", "time", "value", "variable"])
    imports = pd.DataFrame(imports, columns=["region", "time", "value", "variable"])


    storageout_df = db[classes.str.startswith("Storage Out")]

    storagein_df = db[classes.str.startswith("Storage In")]

    agg_df = pd.concat([supply_df, imports, exports, storagein_df, storageout_df])

    agg_df.fillna(0, inplace=True)
    # # map names if in dict utils.tech_agg_COPPER else leave as is

    agg_df["region"] = agg_df.region.map(utils.province_short).fillna(agg_df.region)

    # only take the first two letters if the region name and capitalize it
    agg_df["region"] = agg_df.region.apply(lambda x: x[:2].upper())

    # sum up same variable, time, hour, region
    agg_df = agg_df.groupby(["variable", "time", "region"]).sum().reset_index()

    # value MW to GW
    agg_df["value"] = agg_df.value.apply(lambda x: x / 1000)

    agg_df["scenario"] = scenario

    # time as datetime
    agg_df["time"] = pd.to_datetime(agg_df["time"])
    agg_df["time"] = agg_df["time"] - pd.Timedelta(hours=1)
    # for leap years adjust each time entry that is after February
    agg_df.loc[agg_df["time"].dt.is_leap_year & (agg_df["time"].dt.month > 2), "time"] += pd.DateOffset(days=1)

    # create period column which is int year
    agg_df["period"] = agg_df["time"].dt.year
    agg_df["period"] = agg_df["period"].astype(int)

    return agg_df



def process(selected):
    """
    Process dispatch data from multiple scenarios.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario, db in selected.items():
        dfs.append(aggregate_db(db, scenario))
    full_data =  pd.concat(dfs)
    can_data = full_data.groupby(["variable", "time", 'period', "scenario"]).sum().reset_index()
    can_data["region"] = "CAN"

    # make period column just the year
    can_data["period"] = can_data["time"].dt.year
    can_data["period"] = can_data["period"].astype(int)
    full_data['period'] = full_data['time'].dt.year
    full_data['period'] = full_data['period'].astype(int)
    return pd.concat([full_data, can_data])
