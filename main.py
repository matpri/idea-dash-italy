import dash
import dash_lumino_components as dlc
from dash import html

from callbacks import modal_handling, tab_handling, burger_handling, sidebar_handling, data_viewer_handling
from components import ids, header, plot_canvas, sidebar
from components.data_selection import data_modal
from utils.data_handler import DataHandler

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
]
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

data_handler: DataHandler = DataHandler()
# link profile callbacks to app
data_handler.link(app)
print('Profiles Found:', data_handler.profiles)
modal_handling.link(app)
tab_handling.link(app)
burger_handling.link(app)
sidebar_handling.link(app)
data_viewer_handling.link(app)

app.layout = html.Div([
    header.render(app),
    html.Div([
        dlc.BoxPanel([
            plot_canvas.render(app),
        ], id='test', addToDom=True),
        sidebar.render(),
        data_modal.render(app),
        # component to represent data change (hidden)
        html.Button('Change Data', id=ids.DATA_CHANGE, style={'display': 'none'}),

    ], id=ids.CONTENT)
])


if __name__ == '__main__':
    app.run(debug=True)
