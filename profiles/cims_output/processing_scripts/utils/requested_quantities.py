import pandas as pd
import os

from profiles.cims_output import utils


def check(df):
    """
    Check if 'Results_summary_carbon_AP_tech' is present in the 'variable' column.

    Parameters:
        df (pd.DataFrame): The DataFrame to check.

    Returns:
        bool: True if the specified prefix is found, False otherwise.
    """
    #print("Checking for emissions in variable column")
    try:
        if (df.model == 'CIMS').any():
            if (df.parameter == 'requested_quantities').any():
                return True
        return False
    except Exception as e:
        print("Emission check", e)
        return False


def recursive_search(df, service, visited=None):
    if visited is None:
        visited = set()
    if service in visited:
        print(f'Recursive loop detected at {service}')
        return ''
    visited.add(service)

    if service not in df['full_path'].unique():
        print(f'{service} not found')
        return ''

    tree_dict = {}
    targets = df[df['full_path'] == service]['target'].unique()
    print(service, targets)

    for target in targets:
        tree_dict[target] = recursive_search(df, target, visited)

    return tree_dict if tree_dict else ''


def dict_to_df(nested_dict, parent_service=None):
    rows = []

    def traverse_dict(d, parent):
        for key, value in d.items():
            rows.append({"service": key, "parent_service": parent})
            if isinstance(value, dict):
                traverse_dict(value, key)

    traverse_dict(nested_dict, parent_service)

    df = pd.DataFrame(rows)

    # fill None with ''
    df = df.fillna('')
    return df

def process(selected: dict):
    dfs = []
    for scenario_name, db in selected.items():
        df = db.copy()

        requested_services = df[(df['parameter'] == 'service requested')].copy()

        # remove nan sectors
        requested_services = requested_services[requested_services['sector'].notna()]
        sectors = requested_services['sector'].unique()
        parents = []
        for sector in sectors:
            requested_service = requested_services[(requested_services['sector'] == sector)]
            start_service = requested_service[requested_services['short_path'] == sector]['full_path'].values[0]
            tree = {start_service: recursive_search(requested_service, start_service)}
            parents.append(dict_to_df(tree))

        parent_services = pd.concat(parents)


        # filter where 'Results_summary_carbon_AP_tech|' in variable column entry and remove the prefix

        distributed_supply = df[(df['parameter'] == 'distributed_supply') & (df['target'].str.endswith('Electricity'))][
            ['sector', 'target', 'short_path', 'value_num']]
        distributed_supply = distributed_supply.rename(columns={'value_num': 'distributed_supply'})

        df = df[(df['parameter'] == 'requested_quantities') & (df['technology'].isna())]
        df = df.merge(distributed_supply, on=['sector', 'target', 'short_path'], how='left')
        df['distributed_supply'] = df['distributed_supply'].fillna(0)
        df['value_num'] = df['value_num'] - df['distributed_supply']
        df = df.drop(columns=['distributed_supply'])

        df = df[~df['region'].str.contains('CAN')]
        df['short_path'] = df['short_path'].fillna('')
        layers = df['short_path'].apply(lambda x: len(x.split('.'))).max()

        # create a column for each layer
        for i in range(layers):
            df[f'layer_{i}'] = df['short_path'].apply(
                lambda x: x.split('.')[i] if len(x.split('.')) > i else '')
        df['scenario'] = scenario_name
        df = df.merge(parent_services, left_on='full_path', right_on='service', how='left')

        # for each entry find the difference between full_path and short_path and remove the prefix from service and parent_service
        # make service and parent_service columns strings if nan and fill with ''
        df['service'] = df['service'].fillna('')
        df['parent_service'] = df['parent_service'].fillna('')
        df['service'] = df['service'].astype(str)
        df['parent_service'] = df['parent_service'].astype(str)
        for i, row in df.iterrows():
            prefix = row['full_path'].replace(row['short_path'], '')
            df.at[i, 'service'] = row['service'].replace(prefix, '')
            df.at[i, 'parent_service'] = row['parent_service'].replace(prefix, '')
        dfs.append(df)
    full_df = pd.concat(dfs)
    return full_df
