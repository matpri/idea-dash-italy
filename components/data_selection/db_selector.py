import dash_mantine_components as dmc
from dash import html

def render():
    from main import data_handler
    data = []
    for i, row in data_handler.runs.iterrows():
        data.append(
            {
                "label": dmc.Group(
                    [
                        dmc.Text(
                            row.model,
                            size='sm',
                            weight=500
                        ),
                        dmc.Divider(orientation="vertical", style={"height": 20, "margin": "0 10px"}),
                        dmc.Text(
                            row.scenario,
                            size='sm',
                            weight=400
                        ),
                        dmc.Divider(orientation="vertical", style={"height": 20, "margin": "0 10px"}),
                        dmc.Text(
                            row.author,
                            size='md',
                            weight=300
                        )
                    ],
                    position='apart'
                ),
                "value": f'{row.model}-{row.scenario}-{row.author}'
            }
        )

    layout = html.Div(
        [
            dmc.CheckboxGroup(
                id='db-checkboxes',
                label='Select runs',
                orientation='vertical',
                value=[],
                children=[
                    dmc.Checkbox(
                        label=row['label'],
                        value=row['value'],
                        style={
                            'margin': '10px',
                            'background': 'rgba(47,146,231,0.2)',
                            'border-radius': '10px',
                            'backdrop-filter': 'blur(5px)',
                            'box-shadow': '0 4 30px 0 rgba(128, 128, 128, 0.2)',
                            'border': '1px solid rgba(47,146,231, 0.3)',
                            '-webkit-backdrop-filter': 'blur(5px)',
                        }
                    )
                    for row in data
                ]
            ),
        ],
        id='db-selector',
        style={
            "maxHeight": "300px",
            "width": "100%",
            'display': 'block',
            'background-color': '#F8F8F8',
            'border-radius': '10px',
            'padding': '20px',
            'margin': '10px',
            'box-shadow': '0 1px 5px 0 rgba(0, 0, 0, 0.1)',
        }
    )
    return layout
