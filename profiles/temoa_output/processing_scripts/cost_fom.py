import pandas as pd
import os

from openpyxl.reader.excel import load_workbook

from profiles.temoa_output import utils
def check(df):
    """
    Check if 'cost' is present in the 'variable' column.

    Args:
        df (DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for cost in variable column")
    try:
        if (df.model == 'Sutubra').any():
            if df.variable.str.startswith("Capital|FO&M costs (nom_undisc)|").any():
                return df[df.variable.str.startswith("Capital|FO&M costs (nom_undisc)|")]['value'].sum() != 0
        return False
    except Exception as e:
        print("cost check", e)
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


def aggregate_technologies(df):
    """
    Aggregate technologies in the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Aggregated data.
    """
    df = df.copy()
    df = df.groupby(["variable", "region", "time"]).sum(numeric_only=True).reset_index()
    return df.sort_values(["region", "time", "variable"])

def calculate_fom(fom_df):
    """
    Calculates the fixed operating and maintenance (FOM) cost data from the DataFrame.

    Args:
        df (DataFrame): Input DataFrame containing cost data.

    Returns:
        DataFrame: Calculated FOM cost data.

    """
    # fom_df = df[df['variable'].isin(utils.fom_names)].copy()

    fom_df['variable'] = fom_df['variable'].map(utils.cost_tech).fillna(fom_df['variable'])
    fom_df['variable'] = fom_df['variable'].apply(lambda x: 'Transmission' if 'Transmission' in x else x)
    fom_df.sort_values(by=["region", "time", 'variable'])
    fom_df = fom_df.groupby(["variable", "region", "time", "scenario"]).sum(numeric_only=False).reset_index()

    # Aggregate data over all regions by variable, time, and scenario and sum the values
    can_fom_df = fom_df.groupby(["variable", "time", "scenario"], as_index=False).sum(numeric_only=True)

    # Add a row with "Region" as "CAN"
    can_fom_df = can_fom_df.assign(region='CAN')

    # Concatenate the original DataFrame and the aggregated DataFrame
    fom_df = pd.concat([fom_df, can_fom_df], ignore_index=True)
    return fom_df
def process(data):
    """
    Process emission data from multiple scenarios based on the 'folders' dictionary.

    Parameters:
        folders (dict): Dictionary containing scenario names as keys and folder paths as values.
        target_dir (str): Target directory.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    dfs = []
    for scenario_name, db in data.items():
        df = db.copy()
        df = df[df.variable.str.startswith("Capital|FO&M costs (nom_undisc)|")]
        df['variable'] = df['variable'].apply(lambda x: '|'.join(x.split("|")[2:]))
        formatted_df = format_df(df)
        df = calculate_fom(formatted_df)
        df['scenario'] = scenario_name
        dfs.append(df)
    full_df = pd.concat(dfs)
    full_df['unit'] = '$ Billions'
    full_df['value'] = full_df['value'].div(1e9)
    
    return full_df
