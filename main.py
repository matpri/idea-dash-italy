import webbrowser
from threading import Timer

import dash
import dash_lumino_components as dlc
from dash import html

from callbacks import modal_handling, tab_handling, burger_handling, sidebar_handling, data_viewer_handling, \
    plot_handling, help_handling
from components import ids, header, plot_canvas, sidebar
from components.data_selection import data_modal, selected_files
from components.help import help
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
plot_handling.link(app)
help_handling.link(app)
selected_files.link(app)

app.layout = html.Div([
    header.render(app),
    html.Div([
        dlc.BoxPanel([
            plot_canvas.render(),
        ], id='test', addToDom=True),
        sidebar.render(),
        data_modal.render(app),
        help.render(),

        # component to represent data change (hidden)
        html.Button('Change Data', id=ids.DATA_CHANGE, style={'display': 'none'}),
        html.Button('Update chips', id=ids.UPDATE_CHIPS, style={'display': 'none'}),
        html.Button('Change Settings', id=ids.SETTINGS_CHANGE, style={'display': 'none'}),
        html.Button('Change Data', id=ids.AFTER_CHANGE, style={'display': 'none'}),

    ], id=ids.CONTENT,
    )
])


def open_browser(port:int):
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    port = 8050  # or simply open on the default `8050` port
    Timer(1, open_browser, args=[port]).start()
    app.run_server(port=port)
