import pandas as pd


def check(df):
    # check if emissions in variable column which has strings like transmission|AB -> BC, emissions|coal etc.
    print("Checking for total_vacancies in variable column")
    try:
        classes = df["variable"].apply(lambda x: x.split("|")[0])
        if (classes == 'total_vacancies').any():
            return True
        return False
    except Exception as e:
        print("dispatch check", e)
        return False


def process(selected):
    dfs = []
    for scenario, db in selected.items():
        df = db.copy()
        df = df[df['variable'].str.startswith('total_vacancies')]
        df['variable'] = df['variable'].str.replace('total_vacancies|', '')
        total = df.groupby(['time', 'region', 'scenario', 'unit']).sum().reset_index()
        total['variable'] = 'Total'
        df = pd.concat([df, total])
        df['time'] = pd.to_datetime(df['time'])
        df['scenario'] = scenario
        dfs.append(df)

    return pd.concat(dfs)