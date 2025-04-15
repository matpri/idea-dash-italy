import pandas as pd
import os

from profiles.messageix_output import utils


def check(df):
    """
    Check if 'Carbon Sequestration|' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for Carbon Sequestration in variable column")
    try:
        if (df.model == 'MESSAGEix-Canada').any():
            if df.variable.str.startswith("Carbon Sequestration|").any():
                return True
        return False
    except Exception as e:
        print("Carbon Sequestration check", e)
        return False


def format_df(df):
    """
    Extracts province, year, and other relevant information from column names in the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Formatted data with extracted information.
    """
    df['region'] = df['region'].map(utils.province_short).fillna(df['region'])
    df = df.groupby(['region', 'variable', 'time', 'scenario']).sum(numeric_only=True).reset_index()
    return df


def calc_canadian(df):
    """
    Calculates the Canadian total for each year and technology.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Formatted data with extracted information.
    """
    # Group by period and technology and sum the values
    canadian_total = df.groupby(["time", "variable"]).sum(numeric_only=True).reset_index()
    canadian_total["region"] = "Canada"
    return canadian_total


def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Carbon Sequestration|' in variable column entry and remove the prefix
        df = df[df.variable.str.startswith("Carbon Sequestration|")]
        # canadian_total = calc_canadian(df)

        full_data = df

        full_data['type'] = full_data['variable'].str.split('|').str[1]
        # add levels which is the number of | in the variable name
        full_data['levels'] = full_data['variable'].apply(lambda x: len(x.split('|')))
        full_data['parent'] = full_data['variable'].apply(lambda x: '|'.join(x.split('|')[:-1]))
        full_data['scenario'] = scenario_name
        dfs.append(full_data)
    full_df = pd.concat(dfs)
    full_df['time'] = full_df['time'].astype(int)
    print("Carbon Sequestration processed")
    return full_df