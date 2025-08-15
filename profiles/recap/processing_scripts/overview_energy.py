# import pandas as pd
# from profiles.recap.processing_scripts.utils import requested_quantities

# def check(df):
#     """
#     Check if energy demand data is present in the DataFrame.
    
#     Args:
#         df (DataFrame): The DataFrame to check.
    
#     Returns:
#         bool: True if energy demand data is found, False otherwise.
#     """
#     try:
#         return requested_quantities.check(df)
#     except Exception as e:
#         print("Energy demand overview check error:", e)
#         return False


# def process(data):
#     """
#     Process energy demand data from multiple scenarios for the Energy Demand overview.
    
#     Parameters:
#         data (dict): Dictionary containing scenario names as keys and DataFrames as values.
    
#     Returns:
#         pd.DataFrame: Processed DataFrame containing only energy demand data with 'tab' column set to 'Energy Demand'.
#     """
#     dfs = []
    
#     for scenario_name, db in data.items():
#         # Only process if energy demand data is present
#         if requested_quantities.check(db):
#             # Process the energy demand data
#             df = requested_quantities.process({scenario_name: db})
            
#             # Add the tab identifier for the overview
#             df['tab'] = 'Energy Demand'
            
#             # Append to our list of dataframes
#             dfs.append(df)
    
#     # Combine all energy demand dataframes if any were found
#     if dfs:
#         full_df = pd.concat(dfs, ignore_index=True)
#         return full_df
#     else:
#         # Return empty DataFrame with expected columns if no data found
#         return pd.DataFrame(columns=['tab', 'scenario', 'region', 'year', 'parameter',
#                                     'value_num', 'context', 'sub_context', 'short_path',
#                                     'sector', 'technology', 'fuel'])

import pandas as pd
from profiles.recap.processing_scripts import overview as overview_processing

def check(df):
    """
    Check if energy demand data is present in the DataFrame.
    Uses the same check as the overview processing since we'll filter from there.
    
    Args:
        df (DataFrame): The DataFrame to check.
    
    Returns:
        bool: True if overview data is found (which includes energy demand), False otherwise.
    """
    try:
        # Use the overview check since we'll filter the overview data
        return overview_processing.check(df)
    except Exception as e:
        print("overview energy check error:", e)
        return False

def process(data):
    """
    Process energy demand data by using the overview processing and filtering for energy demand only.
    
    Parameters:
        data (dict): Dictionary containing scenario names as keys and DataFrames as values.
    
    Returns:
        pd.DataFrame: Processed DataFrame containing only energy demand data.
    """
    # First, get the full overview data (which includes emissions, energy demand, and technology stocks)
    full_overview_df = overview_processing.process(data)
    
    # Filter to only keep energy demand data
    energy_df = full_overview_df[full_overview_df['tab'] == 'Energy Demand'].copy()
    
    return energy_df