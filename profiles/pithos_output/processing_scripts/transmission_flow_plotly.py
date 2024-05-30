import os
import pandas as pd

from profiles.pithos_output import utils

def check(df):
    """
    Check if 'transmission' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for transmission in variable column")
    try:
        if (df.model == 'HEC-PITHOS').any():
            if df.variable.str.startswith("Transmission flow|").any():
                return True
        return False
    except Exception as e:
        print("transmission check", e)
        return False

def check_folder(folder):
    """
    Check if 'transmission.csv' exists in the given folder.

    Parameters:
        folder (str): Path to the folder to check.

    Returns:
        bool: True if the condition is met, False otherwise.
    """
    #print("Checking for transmission.csv in folder", folder)
    try:
        if "transmission.csv" not in os.listdir(folder):
            return False
        df = pd.read_csv(os.path.join(folder, "transmission.csv"))
        if 'value' in df.columns:
            return df.value.sum() != 0
        else:
            df = pd.read_csv(os.path.join(folder, "transmission.csv"), header=None)
            return df[4].sum() != 0
    except Exception as e:
        print("transmission check", e)
        return False

connections = ["BC -> AB", "AB -> SK", "SK -> MB", "MB -> ON", "ON -> QC", "QC -> NB", "QC -> NL", "NB -> NS",
               "NS -> PE", "PE -> NL", "NL -> NS", "BC -> USA", "AB -> USA", "SK -> USA", "MB -> USA", "ON -> USA",
               "QC -> USA", "NB -> USA", "NS -> USA", "PE -> USA", "NL -> USA"]

line_name_map = {"AB <-> BC": "BC <-> AB",
                 "SK <-> AB": "AB <-> SK",
                 "MB <-> SK": "SK <-> MB",
                 "ON <-> MB": "MB <-> ON",
                 "QC <-> ON": "ON <-> QC",
                 "NB <-> QC": "QC <-> NB",
                 "NS <-> NB": "NB <-> NS",
                 "PE <-> NS": "NS <-> PE",
                 "NL <-> PE": "PE <-> NL",
                 "NL <-> QC": "QC <-> NL",
                 "NL <-> NS": "NS <-> NL",
}

def split_connection(row):
    """
    Split the 'connection' column into start and end nodes.

    Parameters:
        row (pd.Series): The DataFrame row.

    Returns:
        List: List containing start and end nodes.
    """
    if " -> " in row["connection"]:
        return row["connection"].split(" -> ")
    elif " <- " in row["connection"]:
        return row["connection"].split(" <- ")

def connection(row):
    """
    Create a connection based on 'region' and 'variable'.

    Parameters:
        row (pd.Series): The DataFrame row.

    Returns:
        str: Connection string.
    """
    con = " -> ".join([row['region'], row['variable']])
    if con in connections:
        return con
    else:
        return " <- ".join([row['variable'], row['region']])

def preprocess(transmission, scenario="CER"):
    """
    Preprocess transmission data.

    Parameters:
        transmission (pd.DataFrame): Input DataFrame.
        scenario (str): Scenario name.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    transmission = transmission.drop(columns=['model', 'unit'])
    prov_cord = pd.read_csv('./arrow_coords.csv')

    transmission = transmission.melt(id_vars=['variable', 'region', 'hour', 'model', 'scenario'], var_name='time', value_name='value')
    transmission['time'] = pd.to_datetime(transmission['time'].astype(str) + '-01-01') + pd.to_timedelta(transmission['hour'], unit='h')

    # all times - 1 hour delta
    transmission['time'] = transmission['time'] - pd.Timedelta(hours=1)
    transmission['period'] = transmission['time'].dt.year
    sub_transmission = transmission[transmission['period'] == transmission['period'].min()]
    unique_dates = sub_transmission['time'].dt.date.unique()
    transmission = transmission.drop(columns=['time'])
    transmission = transmission[transmission.value != 0]
    transmission = transmission.groupby(["region", "variable", "period"]).sum().reset_index()
    transmission["region"] = transmission.region.map(utils.province_short)
    transmission["variable"] = transmission.variable.map(utils.province_short)
    transmission = transmission.groupby(["region", "variable", "period"]).sum().reset_index()
    transmission = transmission[transmission.region != transmission.variable]
    transmission['connection'] = transmission.apply(lambda row: connection(row), axis=1)
    transmission["period"] = transmission.period.astype(str)
    transmission["scenario"] = scenario
    transmission["value"] = transmission.value / 1000000
    transmission["value"] = transmission["value"] * 365 / len(unique_dates)
    # prov_cord has columns from_lon, from_lat, to_lon, to_lat and region, variable add the correct from_lon, from_lat, to_lon, to_lat to transmission based on region and variable
    # Merge prov_cord into transmission
    transmission = pd.merge(transmission, prov_cord, how='inner', left_on=['region', 'variable'],
                            right_on=['region', 'variable'])

    transmission['from_lat'] = transmission['from_lat'].astype(float)
    transmission['from_lon'] = transmission['from_lon'].astype(float)
    transmission['period'] = transmission['period'].astype(str)
    transmission['start'] = transmission.apply(lambda row: split_connection(row)[0], axis=1)
    transmission['end'] = transmission.apply(lambda row: split_connection(row)[1], axis=1)
    transmission['line'] = transmission.apply(lambda row: " <-> ".join([row['start'], row['end']]), axis=1)
    transmission['built'] = "new"
    return transmission

def process(selected):
    """
    Process transmission data and derive a DataFrame.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    transmissions = []
    for scenario_name, df in selected.items():
        trs = df.copy()
        trs = trs[trs.variable.str.startswith("Transmission flow|")]
        trs = trs.dropna(axis=1, how='all')
        trs["variable"] = trs["variable"].apply(lambda x: '|'.join(x.split("|")[1:]))
        trs["variable"] = trs.variable.apply(lambda x: x.split(".")[0])
        trs = trs.melt(id_vars=['variable', 'region', 'hour', 'scenario', 'model'], var_name='time',
                                               value_name='value')
        trs['time'] = pd.to_datetime(trs['time'].astype(str) + '-01-01') + pd.to_timedelta(
            trs['hour'], unit='h')
        # all times - 1 hour delta
        trs['time'] = trs['time'] - pd.Timedelta(hours=1)
        trs['period'] = trs['time'].dt.year
        sub_transmission = trs[trs['period'] == trs['period'].min()]
        unique_dates = sub_transmission['time'].dt.date.unique()

        trs['value'] = trs['value'] / 1000
        trs['value'] = trs['value'] * 365 / len(unique_dates)
        # drop time
        trs = trs.drop(columns=['time'])
        # group by region, variable, period
        trs = trs.groupby(["region", "variable", "period"]).sum(numeric_only=True).reset_index()
        trs['scenario'] = scenario_name
        trs["region"] = trs.region.apply(lambda x: x.split(".")[0])
        trs["variable"] = trs.variable.apply(lambda x: x.split("to ")[1])
        # remove where variable == region
        trs = trs[trs.region != trs.variable]
        trs = trs.groupby(["region", "variable", "period", 'scenario']).sum(numeric_only=True).reset_index()
        transmissions.append(trs)
    full_t = pd.concat(transmissions)
    prov_cord = pd.read_csv('./profiles/natem_output/visualization_scripts/utils/arrow_coords.csv')
    full_t['region'] = full_t['region'].map(utils.province_long)
    full_t['variable'] = full_t['variable'].map(utils.province_long)

    full_t['short_region'] = full_t['region'].map(utils.province_short)
    full_t['short_variable'] = full_t['variable'].map(utils.province_short)
    full_t = pd.merge(full_t, prov_cord, how='inner', left_on=['region', 'variable'],
                      right_on=['region', 'variable'])
    full_t['from_lat'] = full_t['from_lat'].astype(float)
    full_t['from_lon'] = full_t['from_lon'].astype(float)
    return full_t