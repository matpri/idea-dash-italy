import pandas as pd
import os

from profiles.messageix_output import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for emissions in variable column")
    try:
        if (df.model == 'MESSAGEix-Canada').any():
            if df.variable.str.startswith("Efficiency|").any():
                return True
        return False
    except Exception as e:
        print("Efficiency check", e)
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
    df = df.groupby(['region', 'variable', 'time', 'scenario']).mean(numeric_only=True).reset_index()
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

def find_type(x, types):
    for t in types:
        if t in x:
            return t

def find_parent(x, variables):
    num_pipes = x.count('|')
    parent = '|'.join(x.split('|')[:2])
    for i in range(num_pipes, 2, -1):
        potential_parent = '|'.join(x.split('|')[:i])
        if potential_parent in variables:
            parent = potential_parent

    return parent

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()
        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix
        df = df[df.variable.str.startswith("Efficiency|")]
        # canadian_total = calc_canadian(df)
        full_data = df
        # add levels which is the number of | in the variable name
        types = full_data['variable'].apply(lambda x: '|'.join(x.split('|')[:2])).unique()
        full_data['type'] = full_data['variable'].apply(lambda x: find_type(x, types))
        full_data['levels'] = full_data.apply(lambda row: len(row['variable'].split('|')) - len(row['type'].split('|')), axis=1)
        variables = full_data['variable'].unique()
        full_data['parent'] = full_data['variable'].apply(lambda x: find_parent(x, variables))
        parents = full_data['parent'].unique()
        parents_level_mapping = {parent: full_data[full_data.parent == parent].levels.min() for parent in parents}
        full_data['levels'] = full_data.apply(lambda row: parents_level_mapping[row['parent']] + 1, axis=1)
        full_data['scenario'] = scenario_name
        dfs.append(full_data)
    full_df = pd.concat(dfs)
    full_df['time'] = full_df['time'].astype(int)
    print("Efficiency processed")
    return full_df
