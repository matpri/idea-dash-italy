import dash_mantine_components as dmc
from dash import html


def render():
    print('rendering start')
    layout = html.Div([
        dmc.Text('Load Data', size='xl', weight=500),
        dmc.Text('To load data, click the "Load Data" button in the header.', size='md', weight=300),
        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),
        dmc.Text('Either Load Data from your local machine or from the IDEA database.', size='md', weight=300),

        dmc.Text('Local Files', size='xl', weight=500),
        dmc.Text('To load data from your local machine, click the "Local File" button.', size='md', weight=300),
        dmc.Text(
            'Either click on the field or drag your files onto the upload area. At the moment IDEA supports COPPER results in PYAM format using our pyam conversion script.',
            size='md', weight=300),
        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),

        dmc.Text('Database', size='xl', weight=500),
        dmc.Text('To load data from the IDEA database, click the "Database" button.', size='md', weight=300),
        dmc.Text(
            'Enter you API key and click "Connect". IDEA is connecting to our results Database, which might take some time to load.',
            size='md', weight=300),
        dmc.Text('Once the data is loaded you can select the runs you want to use and click "Load"', size='md', weight=300),
        dmc.Text('You can also filter the runs by the model, scenario or author.', size='md', weight=300),

        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),

        dmc.Text(
            'Once the data is loaded you can edit the plots that should be generated and change the scenario name.',
            size='md', weight=300),

        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),
        dmc.Text(
            'Click the "Submit" button to finalize your selection which will process the data and load them into the system.',
            size='md', weight=300),

        dmc.Image(src='/assets/help/load_data.png', alt='Load Data', width='100%'),
    ],
    )
    return layout
