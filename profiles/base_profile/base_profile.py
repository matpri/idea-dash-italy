import pandas as pd
from dash import html
import dash_mantine_components as dmc
import multiprocessing as mp


# template class for a base profile with parameters: name, visualizations and unimplented function preprocess

def data_processing_task(profile_name, viz, data, processing_func):
    try:
        data_out = processing_func(data)
    except Exception as e:
        print(f"Error processing data for {profile_name} - {viz}: {e}")
        data_out = pd.DataFrame()

    return profile_name, viz, data_out

class BaseProfile:
    name = 'Base Profile'
    db_name = 'base'
    description = 'A Base profile without any visualizations to define model dashboards'
    viz_options = {}
    data = {}
    plot_order = []
    color = 'gray'
    settings = html.Div(
        [
            dmc.Text('Implement Settings for your profile'),
        ]
    )

    def link(self, app):
        for viz in self.viz_options:
            self.viz_options[viz]['callback'](app)


    def process_data(self, data_collection):
        print('Base collective preprocess')
        wants_overview = False
        args = []
        for viz_option, data in data_collection.items():
            if viz_option == 'overview':
                wants_overview = True
                continue
            args.append((self.name, viz_option, data, self.viz_options[viz_option]['process']))
        with mp.Pool(mp.cpu_count()) as pool:
            processed_data = pool.starmap(data_processing_task, args)


        if wants_overview:
            dfs = []
            for _, viz_option, data in processed_data:
                data['variable'] = viz_option
                dfs.append(data)
            full_df = pd.concat(dfs)

            full_df = full_df[full_df['region'] == 'CAN']
            full_df = full_df.groupby(['scenario', 'variable', 'time']).sum(numeric_only=True).reset_index()
            processed_data.append((self.name, 'Overview', full_df[['scenario', 'variable', 'time', 'value']]))

        return processed_data


