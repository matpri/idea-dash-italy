import os
import webbrowser
from threading import Timer
import argparse  # Import argparse for CLI argument parsing

import dash
import dash_lumino_components as dlc
from dash import html

from callbacks import modal_handling, tab_handling, burger_handling, sidebar_handling, data_viewer_handling, \
    plot_handling, help_handling, save_datahandler, selected_files, database_connection, data_modal as data_modal_callback
from components import ids, plot_canvas, sidebar
from components.data_selection import data_modal
from components.help import help
from utils.data_handler import DataHandler

# Set up argument parser
parser = argparse.ArgumentParser(description='Run the Dash app with optional header display.')
parser.add_argument('--static', type=str, default='False',
                    help='Set to "True" to make page static, i.e. hide header and settings to only keep features that are handled client side, "False" to hide it.')
parser.add_argument('--datahandler', type=str, default=None,
                    help='Name of the datahandler file to load.')
parser.add_argument('--help_popup', type=str, default='False',
                    help='Set to True to show help popup on startup.')
parser.add_argument('--autosave', type=str, default='', help='Set to path including file name to automatically pickle the datahandler after preloading data from the data folder to the path + fname set in the arg.')
args = parser.parse_args()  # Parse the arguments





# Convert string to boolean
static = args.static.lower() == 'true'
help_popup = args.help_popup.lower() == 'true'
print("Initializing the Dash app...")  # Debugging statement
# setting up the app
external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'
]
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets)

# get all files in data folder that end either with csv or xlsx
data_files = [f for f in os.listdir('data') if f.endswith('.csv') or f.endswith('.xlsx')]

# initialize data handler which will deal with all data related operations
data_handler: DataHandler = DataHandler()
if args.datahandler is not None:
    print(f"Loading datahandler from {args.datahandler}")
    data_handler = DataHandler()
    data_handler.load(args.datahandler)
    print(f"Datahandler loaded with {len(data_handler.data)} files.")

# link profile callbacks to app
data_handler.link(app)
modal_handling.link(app)
tab_handling.link(app)
burger_handling.link(app)
sidebar_handling.link(app)
data_viewer_handling.link(app)
plot_handling.link(app)
help_handling.link(app)
selected_files.link(app)
save_datahandler.link(app)
database_connection.link(app)
data_modal_callback.link(app)

print(data_files)
print(bool(data_files))
data_handler.preload_data(data_files)
if args.autosave != '':
    print(f"Autosaving datahandler to {args.autosave}")
    # Ensure the directory exists, but do not create a directory for a file path
    autosave_dir = os.path.dirname(args.autosave)
    if autosave_dir != '' and not os.path.exists(autosave_dir):
        os.makedirs(autosave_dir)
    data_handler.save(args.autosave)  # Save the datahandler to the specified file path

app_layout = [
    html.Div([
        dlc.BoxPanel([
            plot_canvas.render(bool(data_files) or args.datahandler is not None, static),
        ], id='test', addToDom=True),
        sidebar.render(static),
        data_modal.render(app),
        help.render(help_popup),

        # component to represent data change (hidden)
        html.Button('Change Data', id=ids.DATA_CHANGE, style={'display': 'none'}),
        html.Button('Update chips', id=ids.UPDATE_CHIPS, style={'display': 'none'}),
        html.Button('Change Settings', id=ids.SETTINGS_CHANGE, style={'display': 'none'}),
        html.Button('Change Data', id=ids.AFTER_CHANGE, style={'display': 'none'}),

    ], id=ids.CONTENT,
    )
]

app.layout = html.Div(app_layout)


def open_browser(port:int):
    """
    Open a web browser with the specified URL.
    This is used to automatically open the browser when the server is started.

    :return: None
    """
    webbrowser.open_new("http://localhost:{}".format(port))


if __name__ == '__main__':
    print("Starting the application...")  # Debugging statement
    
    port = 8050  # or simply open on the default `8050` port
    Timer(1, open_browser, args=[port]).start()
    app.run_server(host="0.0.0.0", port=port)
