import pandas as pd
from dash import html
import dash_mantine_components as dmc
import multiprocessing as mp


# template class for a base profile with parameters: name, visualizations and unimplented function preprocess

def data_processing_task(profile_name, viz, data, processing_func):
    # try:
    data_out = processing_func(data)
    # except Exception as e:
    #     print(f"Error processing data for {profile_name} - {viz}: {e}")
    #     data_out = pd.DataFrame()

    return profile_name, viz, data_out

class BaseProfile:
    display_name = 'Base Profile'
    name = 'base'
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
        
        # Initialize flags and arguments for processing
        wants_overview = 'Overview' in data_collection
        args = [
            (self.display_name, viz_option, data, self.viz_options[viz_option]['process'])
            for viz_option, data in data_collection.items()
            if viz_option != 'Overview'
        ]

        # Process data using the defined processing function
        processed_data = [data_processing_task(*arg) for arg in args]

        if wants_overview:
            # Prepare dataframes for overview
            dfs = self._prepare_overview_data(processed_data)

            # Combine full data with AB+QC data

            full_df = pd.concat(dfs, ignore_index=True)
            full_df = full_df.groupby(['scenario', 'variable', 'time', 'region']).sum(numeric_only=True).reset_index()

            # Filter and group the final dataframe
            full_df = self._filter_and_group_full_df(full_df)

            # Append overview data to processed data
            processed_data.append((self.display_name, 'Overview', full_df[['scenario', 'variable', 'time', 'value', 'region']]))

        return processed_data

    def _prepare_overview_data(self, processed_data):
        """Prepare dataframes for overview by filtering out imports and exports."""
        dfs = []
        for _, viz_option, data in processed_data:
            if viz_option in ['Dispatch', 'Transmission Flow', 'Transmission Capacity', 'Inputs', 'Input']:
                continue
            df = data.copy()
            df = df[~df.variable.str.contains('Import|Export')]
            df['variable'] = viz_option
            dfs.append(df)
        return pd.concat(dfs)

  

    def _filter_and_group_full_df(self, full_df):
        """Filter and group the full dataframe for final output."""
        full_df = full_df[full_df['region'].isin(['CAN'])]
        return full_df.groupby(['scenario', 'variable', 'time', 'region']).sum(numeric_only=True).reset_index()


