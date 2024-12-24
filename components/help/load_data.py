import dash_mantine_components as dmc
from dash import html, dcc


def render():
    layout = html.Div([
        html.H1('Load Data'),
        html.P(
            'To load data, click the "Load Data" button in the header. Either Load Data from your local machine or from the IDEA database.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/data_modal.gif', style={'width': '100%'})),
            html.H3('Opening Data Loading Window',
                    style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('Local Files'),
        html.P(
            'To load data from your local machine, click the "Local File" button. You can either click on the field or drag your files onto the upload area. At the moment IDEA supports COPPER results in PYAM format using our pyam conversion script.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/data_local.gif', style={'width': '100%'})),
            html.H3('Loading Local Data', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1('Database'),
        html.P(
            'To Load data from the IDEA database, click the "Database" button. Enter your API key and click "Connect". IDEA is connecting to our results Database, which might take some time to load. Once the data is loaded, you can select the runs you want to use and click "Load". You can also filter the runs by the model, scenario or author.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/data_db.gif', style={'width': '100%'})),
            html.H3('Loading Data from Database', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.P(
            'Once the data is loaded, you can edit the plots that should be generated and change the scenario name. Click the "Submit" button to finalize your selection. This will process the data and load them into the system.'),

        html.Div([
            html.Center(html.Img(src='/assets/help/data_edit.gif', style={'width': '100%'})),
            html.H3('Editing Data', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.Div([
            html.Center(html.Img(src='/assets/help/data_submit.gif', style={'width': '100%'})),
            html.H3('Submitting Data', style={'font-size': '15px', 'color': 'gray', 'text-align': 'center'}),
        ]),

        html.H1(' Save and Automatically Load'),
        html.P(
            '''To save your workspace, click the "Save" button in the toolbar. The workspace will be saved and you can load it in by uploading it in the local data section or by starting the program adding the '--datahandler' flag, i.e. `python main.py --datahandler=<path to file>`. \n
            This feature works well when less than 8 scenarios are loaded. If more than 8 scenarios are loaded, use `saver.py` script to save the workspace.\n
            Additionally, if you want to bypass having to load in data by using the interface, add the data you want to load into the `data` folder before starting the program. The data will be loaded automatically when the program starts.''',

        )

    ])

    return layout
