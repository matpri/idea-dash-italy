import dash
from dash import Output, Input, State, MATCH, dcc

from profiles.recap.visualization_scripts.ghg import render_plot
from components import ids

emissions_mapping = {
    'Net Emissions': ['total_cumul_net_emissions', 'emissions_total_cumul_net'],
    'Avoided Emissions': ['total_cumul_avoided_emissions', 'emissions_total_cumul_avoided'],
    'Negative Emissions': ['total_cumul_negative_emissions', 'emissions_total_cumul_negative'],
    'Emitted Emissions': ['total_cumul_net_emissions', 'total_cumul_bio_emissions', 'emissions_total_cumul_bio', 'emissions_total_cumul_net'],
    'Emissions Costs': ['total_cumul_emissions_cost', 'emissions_total_cumul_cost']}


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'Summary',
            'viz': 'Economy-wide Emissions'
        }, 'figure', allow_duplicate=True),
        Output({
            'type': 'recap-ghg-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-ghg-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-ghg-service-widgets',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-ghg-service-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'recap-ghg-service-select',
            'index': MATCH
        }, 'value'),
        Output({
            'type': 'recap-ghg-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'recap-ghg-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'recap-ghg-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'recap-ghg-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-ghg-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'recap-ghg-sector-select',
                'index': MATCH
            },
            'style'
        ),
        Input({
            'type': 'recap-emissions-update',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-representation-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-year-select',
            'index': MATCH
        }, 'value'),
        Input(
            {
                'type': 'recap-ghg-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'recap-ghg-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'recap-ghg-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'recap-ghg-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-service-sector-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-service-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'recap-ghg-emission-select',
            'index': MATCH
        }, 'value'),
        State({
            'type': 'recap-ghg-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'recap-ghg-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'Summary',
            'viz': 'Economy-wide Emissions'
        }, 'figure'),
        State({
            'type': 'recap-ghg-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'recap-ghg-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'recap-ghg-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'recap-ghg-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'recap-ghg-text-switch',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_ghg(_update, _representation, _p_type, _scenarios, _scenario, _regions, _years, _pattern, _text,
                   _download, _sector, _service_sector, _service, _emission, _r_style, _y_style, _canvas, _data, _s_style, _m_style,
                   _pattern_style, _text_style):
        # print('updating ghg plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        _data = data_handler.processed_data['Summary']['Economy-wide Emissions']
        _data = _data[_data['tab'] == 'Emissions']

        services = dash.no_update
        _service_style = dash.no_update

        if 'recap-ghg-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(_data.to_csv, "ghg.csv")
            return _canvas, _r_style, _y_style, _service_style, _service, services,  _data, _s_style, _m_style, _pattern_style, _text_style, dash.no_update


        emissions_list = _data[_data['parameter'].str.contains('emissions')]['parameter'].unique().tolist()
        to_use = emissions_mapping[_emission]
        emissions_list = [e_type for e_type in emissions_list if e_type in to_use]

        if 'recap-ghg-service-sector-select' in trigger_id['type']:
            _data = _data[_data['sector'] == _service_sector]
            services = _data[_data.parameter.isin(emissions_list)]['short_path'].unique().tolist()
            _service = services[0]

        if _representation == 'By Emission':
            _sector_style = {'display': 'block'}
            _service_style = {'display': 'none'}

        elif _representation == 'By Service':
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'block'}
        else:
            _sector_style = {'display': 'none'}
            _service_style = {'display': 'none'}

        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Year', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission, aggregate=True)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Trend Over Years',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission, aggregate=True)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Pie Chart', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector if _representation == 'By Emission' else _service_sector, service=_service,
                                  emissions_list=emissions_list, plot_name=_emission, aggregate=True)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Region', _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector if _representation == 'By Emission' else _service_sector,
                                  service=_service,
                                  emissions_list=emissions_list, plot_name=_emission, aggregate=True)

        return _canvas, _r_style, _y_style, _service_style,services, _service, dash.no_update, _s_style, _m_style, _pattern_style, _text_style, _sector_style
