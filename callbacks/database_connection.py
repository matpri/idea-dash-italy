import json
import urllib.request as urllib

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, Input, Output, State

from components import ids
from components.data_selection import db_selector

def link(app):
    app.callback(
        Output(ids.DATABASE_CONNECT_BUTTON, "disabled"),
        Input(ids.API_KEY_INPUT, "value"),
        prevent_initial_call=True,
    )(enable_button)

    app.callback(
        Output(ids.DATABASE_INPUT, "children"),
        Output(ids.DATABASE_INPUT, "style"),
        Output(ids.DB_CONNECTED, "style"),
        Output('db-checkboxes', 'children'),
        Output('db-checkboxes', 'style'),
        Output(ids.MODEL_SELECT, 'data'),
        Output(ids.SCENARIO_SELECT, 'data'),
        Output(ids.AUTHOR_SELECT, 'data'),
        Output(ids.DB_SELECT, 'data'),
        Input(ids.DATABASE_CONNECT_BUTTON, "n_clicks"),
        State(ids.API_KEY_INPUT, "value"),
        State(ids.DATABASE_INPUT, "children"),
        prevent_initial_call=True,
    )(connect_to_database)

    app.callback(
        Output('db-selector', 'children'),
        Input(ids.MODEL_SELECT, 'value'),
        Input(ids.SCENARIO_SELECT, 'value'),
        Input(ids.AUTHOR_SELECT, 'value'),
        Input(ids.DB_SELECT, 'value'),
    )(get_runs)


def enable_button(api_key):
    print('Enabling button', api_key)
    return api_key is None or api_key == ''


def connect_to_database(n_clicks, api_key, children):
    if n_clicks:
        print('Connecting to database with API key:', api_key)
        try:
            url = 'http://206.12.95.102/results_types?key=' + api_key
            response = json.loads(urllib.urlopen(url).read())
            response.append({'model': 'CEF', 'scenario': 'CEF2023', 'author': 'CER'})
            response.insert(0, {'model': 'CODERS', 'scenario': 'CODERS2024', 'author': 'EMH'})

            runs = pd.DataFrame(response)
            runs['DB'] = 'default'
            try:
                mmcw_url = 'http://206.12.95.102/MMCW_results_types?key=' + api_key
                mmcw_response = json.loads(urllib.urlopen(mmcw_url).read())
                mmcw_runs = pd.DataFrame(mmcw_response)
                mmcw_runs['DB'] = 'MMCW'
                runs = pd.concat([runs, mmcw_runs])

            except Exception as e:
                pass
            from main import data_handler
            data_handler.runs = runs

            checkbox_data = []
            model_select = ['ALL'] + [model for model in runs['model'].unique()]
            scenario_select = ['ALL'] + [scenario for scenario in runs['scenario'].unique()]
            author_select = ['ALL'] + [author for author in runs['author'].unique()]
            db_select = ['ALL'] + ['CODERS'] + data_handler.runs['DB'].unique().tolist()
            for i, row in data_handler.runs.iterrows():
                checkbox_data.append(
                    {
                        "label": dmc.Group(
                            [
                                dmc.Text(
                                    row.model,
                                    size='sm',
                                    weight=500
                                ),
                                dmc.Divider(orientation="vertical", style={"height": 20}),
                                dmc.Text(
                                    row.scenario,
                                    size='sm',
                                    weight=400
                                ),
                                dmc.Divider(orientation="vertical", style={"height": 20}),
                                dmc.Text(
                                    row.author,
                                    size='md',
                                    weight=300
                                )
                            ],
                            position='apart'
                        ),
                        "value": f'{row.model}|{row.scenario}|{row.author}|{row.DB}'
                    }
                )
            checkboxes = [
                dmc.Checkbox(
                    label=row['label'],
                    value=row['value'],
                )
                for row in checkbox_data
            ]

            print(runs)
            data_handler.api_key = api_key
            return dash.no_update, {'display': 'none'}, {'display': 'block'}, checkboxes, {
                "maxHeight": "280px",
                "overflowY": "scroll",
                "width": "100%",
            }, model_select, scenario_select, author_select, db_select
        except Exception as e:
            print(e)
            return children + [dmc.Alert(
                title='Error',
                children='Failed to connect to database. Please check your API key and try again.',
                color='red',
                withCloseButton=True,
                style={'width': '80%', 'marginLeft': 'auto', 'marginRight': 'auto'}
            )], dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    return children, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


def get_runs(model, scenario, author, db):
    from main import data_handler
    runs = data_handler.runs
    if model != 'ALL':
        runs = runs[runs['model'] == model]
    if scenario != 'ALL':
        runs = runs[runs['scenario'] == scenario]
    if author != 'ALL':
        runs = runs[runs['author'] == author]
    if db != 'ALL':
        if db == 'CODERS':
            runs = runs[runs['scenario'] == 'CODERS2024']
        else:
            runs = runs[runs['DB'] == db]

    data = []

    for i, row in runs.iterrows():
        data.append(
            {
                "label": dmc.Group(
                    [
                        dmc.Text(
                            row.model,
                            size='sm',
                            weight=500
                        ),
                        dmc.Divider(orientation="vertical", style={"height": 20}),
                        dmc.Text(
                            row.scenario,
                            size='sm',
                            weight=400
                        ),
                        dmc.Divider(orientation="vertical", style={"height": 20}),
                        dmc.Text(
                            row.author,
                            size='md',
                            weight=300
                        )
                    ],
                    position='apart'
                ),
                "value": f'{row.model}|{row.scenario}|{row.author}|{row.DB}'
            }
        )

    layout = [
        dmc.CheckboxGroup(
            id='db-checkboxes',
            label='Select runs',
            orientation='vertical',
            value=[],
            children=[
                dmc.Checkbox(
                    label=row['label'],
                    value=row['value'],
                )
                for row in data
            ],
            style={
                "maxHeight": "280px",
                "overflowY": "scroll",
                "width": "100%",
            },
        ),
    ]
    return layout