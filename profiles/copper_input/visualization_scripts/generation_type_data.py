import dash_mantine_components as dmc
from dash import html, dcc
import plotly.graph_objects as go



def render_plot(df, scenarios, variable,):
    from profiles.copper_input.utils import plot_settings
    #print('rendering plot', type)
    name = plot_settings['Type Data']['name']
    df_scen = df.copy()
    df_scen = df_scen[df_scen['scenario'].isin(scenarios)]
    df_scen = df_scen[df_scen['variable'].str.startswith(variable)]
    df_scen['variable'] = df_scen['variable'].str.replace(variable + '|', '')

    plot_info = plot_settings['Type Data']['Per Technology']
    title = plot_info['title']
    xaxis = plot_info['x_label']
    yaxis = plot_info['y_label']

    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=xaxis,
        yaxis_title=yaxis,
        template="simple_white",
    )
    for scenario in scenarios:
        df_scen = df_scen[df_scen['scenario'] == scenario]
        fig.add_trace(
            go.Bar(
                x=df_scen['variable'],
                y=df_scen['value'],
                showlegend=True,
                name=scenario,
                hovertemplate=f'Variable: {variable} <br> Scenario: {scenario}' + '<br>Value: %{y:.2f}<br>'
            )
        )

    if df_scen.empty:
        #print("No data available, since the results are all zero.")
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="No data available, since the results are all zero.",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )

    fig.layout.autosize = True
    fig.add_hline(y=0, line_dash="dot", line_color="grey")
    fig.update_layout(legend=dict(
        font=dict(
            size=14,
        )
    ))

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    variables = df['variable'].unique().tolist()
    variables = [var.split('|')[0] for var in variables]
    #unique variables
    variables = list(set(variables))

    widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'copper_input-gentype-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in variables],
            value=variables[0],
            id={
                'type': 'copper_input-gentype-variable-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot( df, scenarios, variables[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'copper_input',
            'viz': 'gentype'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
