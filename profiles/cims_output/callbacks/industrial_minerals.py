import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.cims_output.visualization_scripts.industrial_minerals import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'industrial_minerals'
        }, 'figure'),
        Output({
            'type': 'cims-industrial_minerals-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-variable-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-rep_switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-rep_switch',
            'index': MATCH
        }, 'label'),
        Output({
            'type': 'cims-industrial_minerals-pattern-switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-text-switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-industrial_minerals-variable-select',
            'index': MATCH
        }, 'data'), Output({
            'type': 'cims-industrial_minerals-variable-select',
            'index': MATCH
        }, 'value'),
        Output({
            'type': 'cims-industrial_minerals-download',
            'index': MATCH
        }, 'data'),
        Input({
            'type': 'cims-industrial_minerals-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-rep-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-year-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-variable-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-industrial_minerals-rep_switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-industrial_minerals-pattern-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-industrial_minerals-text-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-industrial_minerals-download-button',
            'index': MATCH
        }, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_plot(plot_type, plot, region, year, variable, scenarios, scenario, rep_switch, pattern_switch,
                    text_switch, download_btn):
        print('Industrial Minerals')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        _data = data_handler.processed_data['CIMS Output']['Industrial Minerals']

        if trigger_id['type'] == 'cims-industrial_minerals-download-button':
            return (dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                    dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                    dcc.send_data_frame(_data.to_csv, "industrial_minerals.csv"))

        _m_style = dash.no_update
        _r_style = dash.no_update
        _y_style = dash.no_update
        _s_style = dash.no_update
        _pattern_style = dash.no_update
        _text_style = dash.no_update
        _v_style = {'display': 'none'} if plot_type == 'Requested Quantities' else {'display': 'block'}

        _rep_switch_style = {'display': 'block'} if plot_type == 'Requested Quantities' else {'display': 'none'}

        if plot == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
        elif plot == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
        elif plot == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}

        rep_switch_label = 'By Fuel' if rep_switch else 'By Sector'

        df_plt = _data[_data['plot'] == plot_type]
        variables = dash.no_update
        if trigger_id['type'] == 'cims-industrial_minerals-plot-select':
            variables = [] if plot_type == 'Requested Quantities' else df_plt['parameter'].unique().tolist()
            if variables:
                variable = variables[0]
            else:
                'Requested Quantities'

        _canvas = render_plot(_data, plot_type, plot, rep_switch, year, region, scenarios, scenario, variable,
                              pattern_switch, text_switch)

        return (_canvas, _r_style, _y_style, _v_style, _rep_switch_style, _m_style, _s_style, rep_switch_label,
                _pattern_style, _text_style, variables, variable, dash.no_update)
