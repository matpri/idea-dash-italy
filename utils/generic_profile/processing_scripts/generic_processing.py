import pandas as pd


def create_check(name, model):
    def check(df):
        print(f"Checking for {name} in variable column")
        try:
            if (df.model == model).any():
                if df.variable.str.startswith(f"{name}|").any():
                    return df[df.variable.str.startswith(f"{name}|")]['value'].sum() != 0
            return False
        except Exception as e:
            print("cost check", e)
        return False
    return check

def create_process(name):
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
            df = df[df.variable.str.startswith(f"{name}|")]
            df['variable'] = df['variable'].apply(lambda x: '|'.join(x.split("|")[1:]))
            if 'time' in df.columns and df['time'].dtype == object:
                df['time'] = pd.to_datetime(df['time'], errors='coerce')

            df['scenario'] = scenario_name
            dfs.append(df)
        full_df = pd.concat(dfs)
        return full_df
    return process