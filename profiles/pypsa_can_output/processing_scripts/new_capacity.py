import pandas as pd

from profiles.pypsa_can_output import utils

def check(df):
    """
    Check if net new capacity is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefixes are found, False otherwise.
    """
    print("Checking for net new cap in variable column")
    try:
        if (df.model == 'PyPSA_CAN').any():
            if df.variable.str.startswith("New generation capacity|").any():
                return True
        return False
    except Exception as e:
        print("net new cap  check", e)
        return False

def process_newcap(prov_df, canada_df, scenario_name):
    """
    Process new capacity data.

    Parameters:
        prov_df (pd.DataFrame): Data for the provinces.
        canada_df (pd.DataFrame): Data for Canada.
        scenario_name (str): Name of the scenario.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    prov_df["region"] = prov_df["region"].apply(lambda x: x.split(".")[0])
    prov_df['region'] = prov_df['region'].map(utils.province_short).fillna(prov_df['region'])

    df = pd.concat([canada_df, prov_df])
    df = df[~df.variable.str.contains('retire')]  # Remove rows containing 'retire' in the 'variable' column
    df['value'] = df['value'].div(1000)  # Convert 'value' to GW from MW
    df = df.groupby(['region', 'variable', 'time']).sum(numeric_only=True).reset_index()
    df['scenario'] = scenario_name

    return df

def process(selected):
    """
    Process new capacity and derive a DataFrame.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    new_caps = []
    for scenario_name, df in selected.items():
        df = df.copy()
        prov_df = df[df.variable.str.startswith("New generation capacity|")]

        prov_df['variable'] = prov_df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
        canada_df = prov_df.groupby(['time', 'scenario', 'variable']).sum(numeric_only=True).reset_index()
        canada_df['region'] = 'CAN'
        new_cap = process_newcap(prov_df, canada_df, scenario_name)

        new_caps.append(new_cap)


    full_data = pd.concat(new_caps)

    full_data['time'] = full_data['time'].astype(int)
    return full_data

