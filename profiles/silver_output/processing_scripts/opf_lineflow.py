import glob
import os

import pandas as pd


def check(df):
    # check if emissions in variable column which has strings like transmission|AB -> BC, emissions|coal etc.
    print("Checking for dispatch, *out and transmission in variable column")
    try:
        if type(df) is pd.DataFrame:
            classes = df[df['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
            if (classes == 'OPF Line Flow').any():
                return True
        else:
            classes = df['data'].keys()
            if any(c.startswith('OPF_Line_Flow') for c in classes):
                return True

        return False
    except Exception as e:
        print("dispatch check", e)
        return False

def aggregate_db(db, scenario):
    classes = db[db['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
    df = db[db['model']=='silver'][classes == 'OPF Line Flow']
    df.drop(columns=['model', "unit"], inplace=True)

    # sum over value and group by time and variable
    df = df.groupby(['region','time', 'variable']).sum().reset_index()
    df['scenario'] = scenario
    df['line'] = df['variable'].apply(lambda x: x.split("|")[1])
    df['region'] = df['line'] + ' -> ' + df['region']
    df['time'] = pd.to_datetime(df['time'])
    df['period'] = df['time'].dt.year.astype(int)
    df = df[['time', 'region', 'value', 'scenario']]
    return df


def process(selected):
    dfs = []
    for scenario, db in selected.items():
        df_processed = aggregate_db(db.copy(), scenario)

        dfs.append(df_processed)

    return pd.concat(dfs)


def process(selected):
    dfs = []
    for scenario, db in selected.items():
        if type(db) is pd.DataFrame:
            df_processed = aggregate_db(db.copy(), scenario)
        else:
            uc_results_var = [k for k in db['data'].keys() if k.startswith('OPF_Results')][0]
            time = db['data']['ts']
            data = db['data'][uc_results_var]
            records = {'time': [], 'region': [], 'value': []}
            for gen in data.keys():
                if gen != 'unit':
                    for t_idx, val in enumerate(data[gen]):
                        records['time'].append(time[t_idx])
                        records['region'].append(gen)
                        records['value'].append(val)

            df = pd.DataFrame.from_dict(records)
            df['time'] = pd.to_datetime(df['time'])
            df['period'] = df['time'].dt.year.astype(int)
            df['scenario'] = scenario
            df_processed = df[['time', 'region', 'value', 'scenario']]

        dfs.append(df_processed)

    return pd.concat(dfs)
