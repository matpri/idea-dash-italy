from dash import html, dcc

from components import ids


def render(app):
    layout = html.Div([
        dcc.Upload(
            id=ids.DATA_UPLOAD,
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '120px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'center',
                'flexDirection': 'column',
                'margin': '10px'
            },
            multiple=True
        ),
        html.Div(id='data-loading-notification'),
    ], id=ids.DATA_LOCAL_INPUT, style={"width": "60%", 'display': 'block'})

    return layout
