import pandas as pd

from profiles.copper_output import utils
def check(df):
    """
    Check if emissions in the 'variable' column contain strings like 'Results_summary_ABA_generation_mix|' or 'Results_summary_Canada_generation_mix|'.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified strings are found, False otherwise.
    """
    #print("Checking for gen cap in variable column")
    try:
        if (df.model == 'OBPS').any():
            if df.variable.str.contains("Standard").any():
                return True
        return False
    except Exception as e:
        print("OBPS standard  check", e)
        return False

def process(dbs: dict):
    """
    Process generation capacity data from multiple scenarios.

    Parameters:
        dbs (dict): Dictionary containing DataFrames for different scenarios.

    Returns:
        pd.DataFrame: Processed generation capacity data.
    """
    dfs = []
    for scenario_name, db in dbs.items():
        df = db.copy()
        df = df[df.variable.str.contains('Standard')]
        df['variable'] = df['variable'].str.replace('Input|Policy|OBPS|Standard|', '')
        df['sector'], df['variable'] = df['variable'].apply(lambda x: x.split('|')[0]), df['variable'].apply(lambda x: '|'.join(x.split('|')[1:]))
        df['scenario'] = scenario_name

        dfs.append(df)

    full_df = pd.concat(dfs)
    full_df['time'] = full_df['time'].astype(int)

    return full_df



