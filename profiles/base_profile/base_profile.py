import pandas as pd
from dash import html
import dash_mantine_components as dmc


# template class for a base profile with parameters: name, visualizations and unimplented function preprocess

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
        processed_data = []
        for viz_option, data in data_collection.items():
            if viz_option == 'overview':
                wants_overview = True
                continue
            processed_data.append((self.name, viz_option, self.viz_options[viz_option]['process'](data)))

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


