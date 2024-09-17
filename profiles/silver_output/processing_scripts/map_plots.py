import pandas as pd

from profiles.silver_output.processing_scripts import opf_emissions, opf_results, opf_curtailment, opf_costs, price_opf, uc_emissions,  uc_curtailment, uc_results

check_funcs = [opf_emissions.db_check, opf_results.db_check, opf_curtailment.db_check, opf_costs.check, price_opf.check, uc_emissions.check, uc_curtailment.db_check, uc_results.check]

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
        # make sure latitude and longitude columns are present
        if not ('latitude' in df.columns or 'longitude' in df.columns):
            return False

        if (df.model == 'silver').any():
            valid = False
            for check_func in check_funcs:
                valid = check_func(df)
                if valid:
                    break
            return valid
        return False
    except Exception as e:
        print("transmission check", e)
        return False


def process(selected):
    dfs = []
    for scenario, db in selected.items():
        df = db.copy()
        df.drop(columns=['model', "unit"], inplace=True, errors='ignore')

        df['classes'] = df["variable"].apply(lambda x: x.split("|")[0])

        for cls in df['classes'].unique():
            # if 'Line Flow' not in cls:
            df_cls = df[df['classes'] == cls]

            # drop columns that are all nan
            df_cls = df_cls.dropna(axis=1, how='all')
            columns = df_cls.columns.tolist()
            columns.remove('value')
            df_cls = df_cls.groupby(columns).sum(numeric_only=True).reset_index()
            df_cls['scenario'] = scenario
            df_cls['time'] = pd.to_datetime(df_cls['time'])
            df_cls['period'] = df_cls['time'].dt.year.astype(int)

            # remove *| from variable
            df_cls['variable'] = df_cls['variable'].apply(lambda x: x.split("|")[-1])

            dfs.append(df_cls)

    return pd.concat(dfs)
