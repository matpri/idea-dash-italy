import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from profiles.silver_output.visualization_scripts.utils import total_plot, tech_plot, region_plot
palette = {

    'LB': '#4B8BBE',
    'NG_CC': '#FFB347',
    'NG_CCS': '#FFD580',
    'NG_CG': '#FF7F50',
    'NG_SC': '#FF6347',
    'PHS': '#4682B4',
    'biomass': '#8FBC8F',
    'coal': '#ad7849',
    'coal_CCS': '#d6aa78',  # dark gray
    'diesel': '#B22222',  # firebrick
    'geothermal': '#20B2AA',  # light sea green
    'h2blue_CT': '#5F9EA0',  # cadet blue
    'h2green_CT': '#3CB371',  # medium sea green
    'hydro_daily': '#1E90FF',  # dodger blue
    'hydro_hourly': '#00BFFF',  # deep sky blue
    'hydro_monthly': '#87CEEB',  # sky blue
    'nuclear': '#9370DB',  # medium purple
    'solar': '#FFD700',  # gold
    'wind': '#37d63b',  # medium spring green
    'infeasibility_padding_generator': '#FF69B4',  # hot pink
    'importexport_scheduled': '#8A2BE2',  # blue violet
    'import': '#4169E1',  # royal blue
    'export': '#F0E68C',  # khaki

    # Generic fallbacks
    'Hydro': '#1E90FF',
    'Coal': '#696969',
    'Gas': '#FFB347',
    'Wind': '#37d63b',
    'Solar': '#FFD700',
    'Nuclear': '#9370DB',
    'Biomass': '#8FBC8F',
    'Geothermal': '#20B2AA',
    'Oil': '#B22222'
}

def render_plot(type, df, scenarios, time_size='hourly'):
    from profiles.silver_output.utils import plot_settings
    print('rendering plot', type)
    name = plot_settings['UC Emissions']['name']
    unit = plot_settings['UC Emissions']['unit']

    title = plot_settings['UC Emissions'][type]['title']
    x_axis_label = plot_settings['UC Emissions'][type]['x_label']
    y_axis_label = plot_settings['UC Emissions'][type]['y_label']
    if type == 'Total':
        fig = total_plot.render(df, scenarios, title, x_axis_label, y_axis_label, time_size)
    elif type == 'By Plant':
        fig = region_plot.render(df, scenarios, title, x_axis_label, y_axis_label, time_size)
    elif type == 'By Technology':
        fig = tech_plot.render(df, scenarios, title, x_axis_label, y_axis_label, time_size)
    else:
        season_order = ['Winter', 'Spring', 'Summer', 'Fall']
        date_type_order = ['Minimum Supply Day', 'Average Supply Day', 'Maximum Supply Day', ]

        seasons = {'Winter': [12, 1, 2], 'Spring': [3, 4, 5], 'Summer': [6, 7, 8], 'Fall': [9, 10, 11]}
        uc_emissions = df[df['scenario'] == scenarios]
        uc_emissions['variable'] = uc_emissions.variable.apply(lambda x: x.split('|')[-1] if '|' in x else x)
        uc_emissions['month'] = uc_emissions['time'].dt.month
        uc_emissions['season'] = uc_emissions['month'].apply(
            lambda x: next((season for season, months in seasons.items() if x in months), 'Unknown'))

        seasoned = []
        for season in seasons.keys():
            print('Processing season:', season)
            uc_season = uc_emissions[uc_emissions['season'] == season].copy()
            try:
                uc_season['day'] = uc_season['time'].dt.dayofyear
                season_daily_supply = uc_season.groupby(['day'], as_index=False)['value'].sum()

                # find day index for min and max using idxmin/idxmax
                min_day_idx = season_daily_supply['value'].idxmin()
                max_day_idx = season_daily_supply['value'].idxmax()

                min_df = uc_season[uc_season['day'] == season_daily_supply.iloc[min_day_idx]['day']][
                    ['value', 'variable']].groupby(by=['variable'], as_index=False).sum()
                min_df['date_type'] = 'Minimum Supply Day'
                max_df = uc_season[uc_season['day'] == season_daily_supply.iloc[max_day_idx]['day']][
                    ['value', 'variable']].groupby(by=['variable'], as_index=False).sum()
                max_df['date_type'] = 'Maximum Supply Day'
                avg = uc_season.groupby(['variable'], as_index=False)['value'].sum()
                avg['value'] /= len(season_daily_supply)
                avg['date_type'] = 'Average Supply Day'

                s_df = pd.concat([pd.DataFrame(min_df), pd.DataFrame(max_df), pd.DataFrame(avg)], ignore_index=True)
                s_df['season'] = season
                seasoned.append(s_df)
            except Exception as e:
                print(f"Error processing season {season}: {e}")
                continue
        seasoned_df = pd.concat(seasoned)

        fig = go.Figure()


        fig.update_layout(
            title=f'{scenarios} - Seasonal supply mix',
            xaxis_title='MWh',
            yaxis_title='Season',
            barmode='relative',
            legend_title='Technology',
            template='plotly_white',
        )
        # ensure season/date_type ordering using categorical dtypes
        season_cat = pd.CategoricalDtype(categories=season_order, ordered=True)
        date_type_cat = pd.CategoricalDtype(categories=date_type_order, ordered=True)

        for gen_type in seasoned_df['variable'].unique():
            df_gen = seasoned_df[(seasoned_df['variable'] == gen_type)].copy()
            df_gen['season'] = pd.Categorical(df_gen['season'], dtype=season_cat)
            df_gen['date_type'] = pd.Categorical(df_gen['date_type'], dtype=date_type_cat)
            # sort using categorical codes to avoid type-checker issues
            df_gen['season_code'] = df_gen['season'].cat.codes
            df_gen['date_code'] = df_gen['date_type'].cat.codes
            # combine into a single sortable key so static checkers don't complain
            df_gen['__sort_key'] = df_gen['season_code'] * 100 + df_gen['date_code']
            # use argsort to avoid static-analysis warnings about sort_values signature
            order = np.argsort(df_gen['__sort_key'].values)[::-1]
            df_gen = df_gen.iloc[order].reset_index(drop=True)
            df_gen = df_gen.drop(columns=['season_code', 'date_code', '__sort_key'])

            y = [df_gen['season'].values, df_gen['date_type'].values]
            fig.add_bar(
                y=y,
                x=df_gen['value'],
                name=gen_type,
                orientation='h',
                marker_color=palette.get(gen_type, 'grey'),  # Default color if not found
                hovertemplate=f'{gen_type}<br>' + '%{y}<br>%{x} MWh<br><extra></extra>',
            )

        fig.update_yaxes(categoryorder='total descending')
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Total', 'By Plant', 'By Technology', 'Seasonal']],
            value='Total',
            id={
                'type': 'silver-uc_emissions-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'silver-uc_emissions-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'silver-uc_emissions-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='hourly',
            id={
                'type': 'silver-uc_emissions-time_step-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Button('Download Data', id={'type': 'silver-uc_emissions-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-uc_emissions-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Total', df, [scenarios[0]]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'SILVER',
            'viz': 'UC Emissions'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
