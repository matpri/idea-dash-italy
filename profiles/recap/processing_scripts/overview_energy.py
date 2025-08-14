import pandas as pd
from profiles.recap.processing_scripts.utils import requested_quantities

def check(df):
    """
    Check if energy demand data is present in the DataFrame.
    
    Args:
        df (DataFrame): The DataFrame to check.
    
    Returns:
        bool: True if energy demand data is found, False otherwise.
    """
    try:
        return requested_quantities.check(df)
    except Exception as e:
        print("Energy demand overview check error:", e)
        return False


def process(data):
    """
    Process energy demand data from multiple scenarios for the Energy Demand overview.
    
    Parameters:
        data (dict): Dictionary containing scenario names as keys and DataFrames as values.
    
    Returns:
        pd.DataFrame: Processed DataFrame containing only energy demand data with 'tab' column set to 'Energy Demand'.
    """
    dfs = []
    
    for scenario_name, db in data.items():
        # Only process if energy demand data is present
        if requested_quantities.check(db):
            # Process the energy demand data
            df = requested_quantities.process({scenario_name: db})
            
            # Add the tab identifier for the overview
            df['tab'] = 'Energy Demand'
            
            # Append to our list of dataframes
            dfs.append(df)
    
    # Combine all energy demand dataframes if any were found
    if dfs:
        full_df = pd.concat(dfs, ignore_index=True)
        return full_df
    else:
        # Return empty DataFrame with expected columns if no data found
        return pd.DataFrame(columns=['tab', 'scenario', 'region', 'year', 'parameter',
                                    'value_num', 'context', 'sub_context', 'short_path',
                                    'sector', 'technology', 'fuel'])