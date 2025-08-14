import pandas as pd
from profiles.recap.processing_scripts.utils import ghg

def check(df):
    """
    Check if emissions data is present in the DataFrame.
    
    Args:
        df (DataFrame): The DataFrame to check.
    
    Returns:
        bool: True if emissions data is found, False otherwise.
    """
    try:
        if ghg.check(df):
            return True
        return False
    except Exception as e:
        print("cost check", e)
        return False

def process(data):
    """
    Process emission data from multiple scenarios for the Emissions overview.
    
    Parameters:
        data (dict): Dictionary containing scenario names as keys and DataFrames as values.
    
    Returns:
        pd.DataFrame: Processed DataFrame containing only emissions data with 'tab' column set to 'Emissions'.
    """
    dfs = []
    for scenario_name, db in data.items():
        if ghg.check(db):
            df = ghg.process({scenario_name: db})
            df['tab'] = 'Emissions'
            dfs.append(df)

    full_df = pd.concat(dfs)
    return full_df
