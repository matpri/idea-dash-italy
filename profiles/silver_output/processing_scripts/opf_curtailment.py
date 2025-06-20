import glob
import os

import pandas as pd


def db_check(df):
    # check if emissions in variable column which has strings like transmission|AB -> BC, emissions|coal etc.
    print("Checking for OPF_Results in variable column")
    try:
        classes = df[df['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
        if (classes == 'OPF_VRE_Curtailment').any():
            return True
        return False
    except Exception as e:
        print("dispatch check", e)
        return False


def aggregate_db(db, scenario):
    classes = db[db['model'] == 'silver']["variable"].apply(lambda x: x.split("|")[0])
    df = db[db['model']=='silver'][classes == 'OPF_VRE_Curtailment']
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
        df_processed = aggregate_db(db.copy(), scenario)

        dfs.append(df_processed)

    return pd.concat(dfs)
