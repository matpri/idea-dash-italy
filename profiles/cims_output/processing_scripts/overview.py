import pandas as pd

from profiles.cims_output.processing_scripts import (ghg, requested_quantities, stock_lcc)

emissions_mapping = {
    'Net Emissions': ['total_cumul_net_emissions',
                      'total_cumul_avoided_emissions',
                      'total_cumul_negative_emissions',
                      'total_cumul_bio_emissions'],
    'Avoided Emissions': ['total_cumul_avoided_emissions'],
    'Negative Emissions': ['total_cumul_negative_emissions'],
    'Emitted Emissions': ['total_cumul_net_emissions', 'total_cumul_bio_emissions'],
    'Emissions Costs': ['total_cumul_emissions_cost']}

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
        if ghg.check(df):
            return True
        if requested_quantities.check(df):
            return True
        if stock_lcc.check(df):
            return True
        return False
    except Exception as e:
        print("cost check", e)
        return False


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
        if ghg.check(db):
            df = ghg.process({scenario_name: db})
            for key, value in emissions_mapping.items():
                emissions = df[df['parameter'].isin(value)].copy()
                emissions['variable'] = key
                emissions = emissions.rename(columns={'value_num': 'value', 'year': 'time'})
                emissions = emissions.groupby(['scenario', 'variable', 'time']).sum(numeric_only=True).reset_index()
                emissions = emissions[['scenario', 'variable', 'time', 'value']]
                dfs.append(emissions)
        if requested_quantities.check(db):
            df = requested_quantities.process({scenario_name: db})
            df = df[(df['technology'].isna()) & (df['context'] != 'Total')].groupby(
                ['region', 'year', 'scenario']).sum(numeric_only=True).reset_index()
            df = df.rename(columns={'value_num': 'value', 'year': 'time'})
            df['variable'] = 'Requested Quantities'
            df = df[['scenario', 'variable', 'time', 'value']]
            dfs.append(df)
        if stock_lcc.check(db):
            df = stock_lcc.process({scenario_name: db})
            stock_parameters = df[df['parameter'].str.contains('stock')]['parameter'].unique().tolist()
            for parameter in stock_parameters:
                stock = df[df['parameter'] == parameter].copy()
                stock['variable'] = parameter
                stock = stock.rename(columns={'value_num': 'value', 'year': 'time'})
                stock = stock.groupby(['scenario', 'variable', 'time']).sum(numeric_only=True).reset_index()
                stock = stock[['scenario', 'variable', 'time', 'value']]
                dfs.append(stock)
            dfs.append(df)

    full_df = pd.concat(dfs)
    full_df = full_df.groupby(['scenario', 'variable','time']).sum(numeric_only=True).reset_index()
    return full_df[['scenario', 'variable', 'time', 'value']]
