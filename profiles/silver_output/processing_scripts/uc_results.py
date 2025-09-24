import glob
import os

import pandas as pd


def check(df):
    # check if emissions in variable column which has strings like transmission|AB -> BC, emissions|coal etc.
    print("Checking for dispatch, *out and transmission in variable column")
    try:
        if type(df) is pd.DataFrame:
            classes = df[df['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
            if (classes == 'UC Results').any():
                return True
        else:
            classes = df['data'].keys()
            if any(c.startswith('UC_Results') for c in classes):
                return True

        return False
    except Exception as e:
        print("dispatch check", e)
        return False



def aggregate_db(db, scenario):
    classes = db[db['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
    df = db[db['model']=='silver'][classes == 'UC Results']
    df.drop(columns=['model', "unit"], inplace=True)

    # sum over value and group by time and variable
    df = df.groupby(['time', 'variable', 'region']).sum().reset_index()
    df['scenario'] = scenario
    df = df[['time', 'variable', 'value', 'region','scenario']]
    df['time'] = pd.to_datetime(df['time'])
    df['period'] = df['time'].dt.year.astype(int)
    return df


def process(selected):
    dfs = []
    for scenario, db in selected.items():
        if type(db) is pd.DataFrame:
            df_processed = aggregate_db(db.copy(), scenario)
        else:
            uc_results_var = [k for k in db['data'].keys() if k.startswith('UC_Results')][0]
            gens = db['data']['generator']
            time = db['data']['ts']
            data = db['data'][uc_results_var]
            print(f"Processing {scenario} with {len(gens)} generators and {len(time)} time steps")
            records = {'time': [], 'variable': [], 'value': []}
            for gen in data.keys():
                if gen != 'unit':
                    for t_idx, val in enumerate(data[gen]):
                        records['time'].append(time[t_idx])
                        records['variable'].append(gens[gen]['type'])
                        records['value'].append(val)

            df = pd.DataFrame.from_dict(records)
            df['time'] = pd.to_datetime(df['time'])
            df['period'] = df['time'].dt.year.astype(int)
            df['region'] = 'N/A'  # No region info in this format
            df['scenario'] = scenario
            df_processed = df[['time', 'variable', 'value', 'region', 'scenario']]

        dfs.append(df_processed)

    return pd.concat(dfs)
