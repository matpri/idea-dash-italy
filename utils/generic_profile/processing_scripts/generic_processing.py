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


def scale_time_data(df):
    """
    Scales the 'time' data in the DataFrame to ensure it represents complete periods.
    This function only processes the 'time' column if it is a datetime object.
    If 'time' is a datetime object, it checks the frequency and scales accordingly.
    """
    classes = df['variable'].unique()
    cls_df = []
    for class_name in classes:
        class_df = df[df['variable'] == class_name].copy()
        if class_df['time'].apply(lambda x: isinstance(x, pd.Timestamp)).all():
            freq = class_df['time'].diff().mean()
            if freq < pd.Timedelta('1D'):
                class_df['time'] = class_df['time'].dt.floor('D')
                # count the number of unique times for each year
                time_counts = class_df['time'].dt.year.copy().reset_index()

                time_counts['value'] = 1
                time_counts = time_counts.groupby('time').sum().reset_index()
                class_df['time'] = class_df['time'].dt.year

                # group by year and scenario and the sum of the values
                class_df = class_df.groupby(['scenario', 'variable', 'region', 'time']).sum().reset_index()
                # we should scale the values by the number of unique times in each year
                for year in time_counts['time'].unique():
                    counts = time_counts[time_counts['time'] == year]
                    if year % 4 == 0:
                        class_df.loc[class_df['time'] == year, 'value'] = class_df.loc[
                                                                              class_df['time'] == year, 'value'] / 366 * \
                                                                          counts['value'].values[0]
                    else:
                        class_df.loc[class_df['time'] == year, 'value'] = class_df.loc[
                                                                              class_df['time'] == year, 'value'] / 365 * \
                                                                          counts['value'].values[0]
            elif freq < pd.Timedelta('1W'):
                class_df['time'] = class_df['time'].dt.floor('W')
                time_counts = class_df['time'].dt.year.copy().reset_index()
                time_counts['value'] = 1
                time_counts = time_counts.groupby('time').sum().reset_index()
                class_df['time'] = class_df['time'].dt.year

                class_df = class_df.groupby(['scenario', 'variable', 'region', 'time']).sum().reset_index()

                for year in time_counts['time'].unique():
                    counts = time_counts[time_counts['time'] == year]
                    class_df.loc[class_df['time'] == year, 'value'] = class_df.loc[
                                                                          class_df['time'] == year, 'value'] / 52 * \
                                                                      counts['value'].values[0]
            elif freq < pd.Timedelta(days=30):
                class_df['time'] = class_df['time'].dt.floor('M')
                time_counts = class_df['time'].dt.year.copy().reset_index()
                time_counts['value'] = 1
                time_counts = time_counts.groupby('time').sum().reset_index()
                class_df['time'] = class_df['time'].dt.year

                class_df = class_df.groupby(['scenario', 'variable', 'region', 'time']).sum().reset_index()

                for year in time_counts['time'].unique():
                    counts = time_counts[time_counts['time'] == year]
                    class_df.loc[class_df['time'] == year, 'value'] = class_df.loc[
                                                                          class_df['time'] == year, 'value'] / 12 * \
                                                                      counts['value'].values[0]
            else:
                class_df['time'] = class_df['time'].dt.year
                class_df = class_df.groupby(['scenario', 'variable', 'region', 'time']).sum().reset_index()
        cls_df.append(class_df)

    df = pd.concat(cls_df)
    # only keep year and turn it into an int
    return df

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

            if 'time' in df.columns:
                df = scale_time_data(df)

            df['scenario'] = scenario_name
            dfs.append(df)
        full_df = pd.concat(dfs)
        return full_df
    return process