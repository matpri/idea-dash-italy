import os
import pandas as pd

from profiles.copper_output import utils

def check(df):
    """
    Check if capacity_transmission is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    print("Checking for capacity_transmission in variable column")
    try:
        if df.variable.str.startswith("Total Transmission|").any():
            return True
        return False
    except Exception as e:
        print("capacity_transmission check", e)
        return False

def check_folder(folder):
    """
    Check if capacity_transmission.csv exists in the given folder.

    Parameters:
        folder (str): Path to the folder to check.

    Returns:
        bool: True if the condition is met, False otherwise.
    """
    print("Checking for capacity_transmission.csv in folder", folder)
    try:
        if "capacity_transmission.csv" not in os.listdir(folder):
            return False

        df = pd.read_csv(os.path.join(folder, "capacity_transmission.csv"))
        if 'value' in df.columns:
            return df.value.sum() != 0
        else:
            df = pd.read_csv(os.path.join(folder, "capacity_transmission.csv"), header=None)
            return df[3].sum() != 0
    except Exception as e:
        print("transmission capacity check", e)
        return False

line_name_map = {
    "AB <-> BC": "BC <-> AB",
    "SK <-> AB": "AB <-> SK",
    "MB <-> SK": "SK <-> MB",
    "ON <-> MB": "MB <-> ON",
    "QC <-> ON": "ON <-> QC",
    "NB <-> QC": "QC <-> NB",
    "NS <-> NB": "NB <-> NS",
    "PE <-> NS": "NS <-> PE",
    "NL <-> PE": "PE <-> NL",
    "NL <-> QC": "QC <-> NL",
    "NL <-> NS": "NS <-> NL",
}

def extant_process(fname):
    """
    Process existing transmission data.

    Parameters:
        fname (str): File name of the existing transmission data.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = pd.read_csv(fname)
    df['region'] = df['ABA'].str.split('.').str[0]
    df['variable'] = df['ABA'].str.split('.').str[2]
    df = df.drop(columns=['ABA'])
    df = pd.melt(df, id_vars=['region', 'variable'], var_name='time', value_name='value')
    df = df.groupby(['time', 'region', 'variable']).sum().reset_index()
    return df

def preprocess(df, scenario):
    """
    Preprocess transmission data.

    Parameters:
        df (pd.DataFrame): Input DataFrame.
        scenario (str): Scenario name.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    df = df.drop(columns=['unit', 'model'])
    prov_cord = pd.read_csv('./province_coordinates.csv', header=0)
    df = df[df['value'] != 0]
    df['region'] = df['region'].str.split('.').str[0]
    df['variable'] = df['variable'].str.split('.').str[0]
    df = df.groupby(['time', 'region', 'variable']).sum().reset_index()
    df["built"] = 'new'
    df.time = df.time.astype(str)
    df['region'] = df['region'].map(utils.province_short).fillna(df['region'])
    df['variable'] = df['variable'].map(utils.province_short).fillna(df['variable'])
    df['line'] = df['region'] + ' <-> ' + df['variable']
    df['line'] = df['line'].map(line_name_map).fillna(df['line'])
    df['scenario'] = scenario
    df['value'] = df['value'] / 1000
    df['larrow'] = 0
    df['rarrow'] = 0

    for index, row in df.iterrows():
        from_line, to_line = row['line'].split(' <-> ')
        if from_line != row['region']:
            df.loc[index, 'larrow'] = df.loc[index, 'value']
            df.loc[index, 'rarrow'] = 0
            df.loc[index, 'region'] = from_line
            df.loc[index, 'variable'] = to_line
        else:
            df.loc[index, 'rarrow'] = df.loc[index, 'value']
            df.loc[index, 'larrow'] = 0

    df = df[df['region'] != df['variable']]
    df = df.groupby(['time', 'region', 'variable', 'line', 'scenario', 'built']).sum().reset_index()

    rarrow = df[df['rarrow'] != 0]
    larrow = df[df['larrow'] != 0]
    rarrow = rarrow.drop(columns=['larrow', 'value'])
    larrow = larrow.drop(columns=['rarrow', 'value'])
    df = pd.merge(rarrow, larrow, on=['time', 'region', 'variable', 'line', 'scenario', 'built'], how='outer')
    df = df.fillna(0)
    df['value'] = df['rarrow']
    df['from_lat'] = df['region'].map(prov_cord.set_index('province')['lat'])
    df['from_lon'] = df['region'].map(prov_cord.set_index('province')['long'])
    df['to_lat'] = df['variable'].map(prov_cord.set_index('province')['lat'])
    df['to_lon'] = df['variable'].map(prov_cord.set_index('province')['long'])
    df.loc[df.variable == 'USA', 'to_lon'] = df['from_lon']
    df.loc[df.variable == 'USA', 'to_lat'] = df['from_lat'] - 10
    df.loc[df.region == 'USA', 'from_lon'] = df['to_lon']
    df.loc[df.region == 'USA', 'from_lat'] = df['to_lat'] - 10
    df['from_lat'] = df['from_lat'].astype(float)
    df['from_lon'] = df['from_lon'].astype(float)

    times = df['time'].unique().tolist()
    cum_ls = []

    for i in range(1, len(times)):
        prev_times = times[:i]
        new_built = df[(df['time'].isin(prev_times)) & (df['built'] == 'new')]
        columns = [*new_built.columns]
        columns.remove('value')
        columns.remove('larrow')
        columns.remove('rarrow')
        new_built = new_built.groupby(columns).sum().reset_index()
        new_built['time'] = times[i]
        new_built['built'] = 'existing'
        cum_ls.append(new_built)

    cum_df = pd.concat(cum_ls)
    df = pd.concat([df, cum_df], ignore_index=True)
    df['value'] = df['rarrow']
    df['scenario'] = scenario
    return df

def process(selected):
    """
    Process transmission data and derive a DataFrame.

    Parameters:
        selected (dict): Dictionary containing scenarios as keys and corresponding DataFrames as values.

    Returns:
        pd.DataFrame: Processed DataFrame.
    """
    transmissions = []
    for scenario_name, db in selected.items():
        df = db.copy()
        df = df[df.variable.str.startswith("Total Transmission|")]
        df['variable'] = df['variable'].apply(lambda x: x.split("|")[1])
        df = df.rename(columns={"time": "period"})
        df = df.sort_values(by=['period'])
        times = df['period'].unique().tolist()
        times.sort()
        # rename time to period
        # sort by region, variable, period
        df["region"] = df.region.apply(lambda x: x.split(".")[0])
        df["variable"] = df.variable.apply(lambda x: x.split(".")[0])
        # remove where variable == region
        df = df[df.region != df.variable]
        df = df.groupby(["region", "variable", "period", 'scenario']).sum(numeric_only=True).reset_index()

        cum_ls = []
        for i in range(1, len(times)):
            prev_times = times[:i]
            new_built = df[(df['period'].isin(prev_times))]
            columns = [*new_built.columns]
            columns.remove('value')
            new_built['period'] = times[i]
            new_built = new_built.groupby(columns).sum().reset_index()
            cum_ls.append(new_built)

        cum_df = pd.concat(cum_ls)
        df = pd.merge(df, cum_df, on=['region', 'variable', 'period', 'scenario'], how='outer')
        df = df.rename(columns={"value_x": "value", "value_y": "cumsum"})
        df['cumsum'] = df['cumsum'].fillna(0)
        df['value'] = df['value'].fillna(0)
        df['total'] = df['value'] + df['cumsum']
        # if os.path.exists(os.path.join(folder, 'extant_transmission.csv')):
        #     extant_df = extant_process(os.path.join(folder, 'extant_transmission.csv'))
        #     extant_df = extant_df.rename(columns={"time": "period"})
        #     df = pd.concat([df, extant_df], ignore_index=True)

        df['scenario'] = scenario_name
        df['period'] = df['period'].astype(int)
        df = df.groupby(["region", "variable", "period", 'scenario', ]).sum(numeric_only=True).reset_index()
        df['value'] = df['value'] / 1000
        df['total'] = df['total'] / 1000
        df['cumsum'] = df['cumsum'] / 1000

        transmissions.append(df)

    full_t = pd.concat(transmissions)
    years = full_t['period'].unique().tolist()
    years.sort()
    scenarios = full_t['scenario'].unique().tolist()
    for scenario in scenarios:
        for i, year in enumerate(years):
            df = full_t[(full_t['scenario'] == scenario) & (full_t['period'] == year)]
            if df.empty and i > 0:
                prev_time = years[i - 1]
                prev_df = full_t[(full_t['scenario'] == scenario) & (full_t['period'] == prev_time)]
                if not prev_df.empty:
                    prev_df['period'] = year
                    prev_df['cumsum'] = prev_df['total']
                    prev_df['value'] = 0
                    full_t = pd.concat([full_t, prev_df], ignore_index=True)
    prov_cord = pd.read_csv('./profiles/copper_output/visualization_scripts/utils/arrow_coords.csv')
    full_t['short_region'] = full_t['region'].map(utils.province_short)
    full_t['short_variable'] = full_t['variable'].map(utils.province_short)
    full_t = pd.merge(full_t, prov_cord, how='inner', left_on=['region', 'variable'],
                  right_on=['region', 'variable'])
    full_t['from_lat'] = full_t['from_lat'].astype(float)
    full_t['from_lon'] = full_t['from_lon'].astype(float)
    return full_t
