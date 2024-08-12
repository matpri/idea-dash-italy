import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.cims_output.visualization_scripts.requested_quantities import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'requested_quantities'
        }, 'figure'),
        Output({
            'type': 'cims-requested_quantities-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-fuel-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-sector-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-requested_quantities-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-requested_quantities-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'cims-requested_quantities-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'cims-requested_quantities-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Input({
            'type': 'cims-requested_quantities-representation-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-year-select',
            'index': MATCH
        }, 'value'),
        Input(
            {
                'type': 'cims-requested_quantities-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'cims-requested_quantities-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'cims-requested_quantities-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'cims-requested_quantities-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-requested_quantities-fuel-select',
            'index': MATCH
        }, 'value'),
        State({
            'type': 'cims-requested_quantities-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-requested_quantities-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'figure',
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'requested_quantities'
        }, 'figure'),
        State({
            'type': 'cims-requested_quantities-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'cims-requested_quantities-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-requested_quantities-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'cims-requested_quantities-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'cims-requested_quantities-text-switch',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_requested_quantities(_representation, _p_type, _scenarios, _scenario, _regions, _years, _pattern, _text,
                         _download, _sector, _service, _fuel ,_r_style, _y_style, _canvas, _data, _s_style, _m_style, _pattern_style, _text_style):
        #print('updating requested_quantities plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'cims-requested_quantities-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(data_handler.processed_data['CIMS Output']['Requested Quantities'].to_csv, "requested_quantities.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _pattern_style, _text_style

        services = dash.no_update
        if 'cims-requested_quantities-sector-select' in trigger_id['type']:
            _data = data_handler.processed_data['CIMS Output']['Requested Quantities']
            _data = _data[_data['sector'] == _sector]
            services = _data[_data['technology'].isna()]['short_path'].unique().tolist()

        if _representation == 'By Sector':
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'none'}
            _fuel_style = {'display': 'block'}

        elif _representation == 'By Service':
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'none'}
            _fuel_style = {'display': 'block'}

        else:
            _sector_style = {'display': 'block'}
            _service_style = {'display': 'block'}
            _fuel_style = {'display': 'none'}

        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation,'By Year', data_handler.processed_data['CIMS Output']['Requested Quantities'],
                                       _scenarios,
                                       _regions,
                                       _years, scenario=_scenario,
                                       pattern_active=_pattern, text_active=_text, sector=_sector, service=_service, fuel=_fuel)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation,'Trend Over Years', data_handler.processed_data['CIMS Output']['Requested Quantities'],
                                       _scenarios,
                                       _regions,
                                       _years, scenario=_scenario, sector=_sector, service=_service, fuel=_fuel)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation,'Pie Chart', data_handler.processed_data['CIMS Output']['Requested Quantities'],
                                       _scenarios,
                                       _regions,
                                       _years, scenario=_scenario, sector=_sector, service=_service, fuel=_fuel)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation,'By Region', data_handler.processed_data['CIMS Output']['Requested Quantities'],
                                       _scenarios,
                                       _regions,
                                       _years, scenario=_scenario,
                                       pattern_active=_pattern, text_active=_text, sector=_sector, service=_service, fuel=_fuel)

        return _canvas, _r_style, _y_style, _fuel_style, _sector_style, _service_style, services, dash.no_update, _s_style, _m_style, _pattern_style, _text_style
