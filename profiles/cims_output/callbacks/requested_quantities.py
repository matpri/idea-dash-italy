import dash
from dash import Output, Input, State, MATCH, dcc, ALL

from profiles.cims_output.visualization_scripts.requested_quantities import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'overview'
        }, 'figure', allow_duplicate=True),
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
            'index': MATCH,
            'layer': ALL
        }, 'style'),
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
        Output({
            'type': 'cims-requested_quantities-representation-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'data'),
        Output({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'value'),

        Input({
            'type': 'cims-demand-update',
            'index': MATCH
        }, 'value'),
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
            'index': MATCH,
            'layer': ALL
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
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'overview'
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
        State({
            'type': 'cims-requested_quantities-representation-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'cims-requested_quantities-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'style'),

        prevent_initial_call=True
    )
    def update_requested_quantities(_update, _representation, _p_type, _scenarios, _scenario, _regions, _years,
                                    _pattern, _text,
                                    _download, _sector, _service, _fuel, _r_style, _y_style, _canvas, _data, _s_style,
                                    _m_style, _pattern_style, _text_style, _p_style, _service_style
                                    ):
        # print('updating requested_quantities plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        _data = data_handler.processed_data['CIMS']['Overview']
        _data = _data[_data['tab'] == 'Energy Demand']

        layers = [dash.no_update] * len(_service_style)
        service_value = _service.copy()
        if 'cims-requested_quantities-download-button' in trigger_id['type']:
            _data = dcc.send_data_frame(_data.to_csv, "requested_quantities.csv")
            return _canvas, _r_style, _y_style, _data,  _s_style, _m_style, _pattern_style, _text_style, _p_style, layers, service_value

        if 'cims-requested_quantities-sector-select' in trigger_id['type']:
            _data = _data[_data['sector'] == _sector]

            layer = 0
            layers = []
            for i in range(layer + 2):
                sub_df = _data.copy()
                for j in range(i):
                    sub_df = sub_df[sub_df['layer_{}'.format(j)] == _service[j]]
                layers.append([{'label': s, 'value': s} for s in sub_df['layer_{}'.format(i)].unique()])

            # pad layers with empty strings to make it same length as _service
            empty_layers = [[]] * (len(_service) - len(layers))
            layers.extend(empty_layers)

            # set _services to '' after layer index
            _service[layer + 1:] = [''] * len(_service[layer + 1:])

        if 'cims-requested_quantities-service-select' in trigger_id['type']:
            _data = _data
            _data = _data[_data['sector'] == _sector]

            layer = trigger_id['layer']
            layers = []
            for i in range(layer + 2):
                sub_df = _data.copy()
                for j in range(i):
                    sub_df = sub_df[sub_df['layer_{}'.format(j)] == _service[j]]
                layers.append([{'label': s, 'value': s} for s in sub_df['layer_{}'.format(i)].unique()])

            # pad layers with empty strings to make it same length as _service
            empty_layers = [[]] * (len(_service) - len(layers))
            layers.extend(empty_layers)

            # set _services to '' after layer index
            _service[layer + 1:] = [''] * len(_service[layer + 1:])

        if _representation == 'By Sector':
            _sector_style = {'display': 'none'}
            _service_style = [{'display': 'none'}] * len(_service_style)
            _fuel_style = {'display': 'block'}

        elif _representation == 'By Service':
            _sector_style = {'display': 'none'}
            _service_style = [{'display': 'none'}] * len(_service_style)
            _fuel_style = {'display': 'block'}

        else:
            _sector_style = {'display': 'block'}
            _fuel_style = {'display': 'none'}

            # find first empty string in _service
            _empty = _service.index('')

            if _empty > 0:
                sub_df = _data.copy()
                sub_df = sub_df[sub_df['sector'] == _sector]
                for i in range(_empty):
                    sub_df = sub_df[sub_df['layer_{}'.format(i)] == _service[i]]
                if len(sub_df['layer_{}'.format(_empty)].unique()) == 1:
                    _empty -= 1

            # make all _service_style block until the first empty string
            _service_style = [{'display': 'block'}] * len(_service_style)
            if _empty < len(_service_style) - 1:
                # make all _service_style none after the first empty string
                _service_style[_empty + 1:] = [{'display': 'none'}] * len(_service_style[_empty + 1:])

        if _p_type == 'Sankey':
            _sector_style = {'display': 'block'}
            _service_style = [{'display': 'none'}] * len(_service_style)
            _fuel_style = {'display': 'none'}

            # remove all empty strings from _service
        service_value = _service.copy()
        _service = [s for s in _service if s]
        _service = '.'.join(_service) if _service else ''

        if _p_type == 'By Year':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _p_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Year',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector, service=_service,
                                  fuel=_fuel)

        elif _p_type == 'Trend Over Years':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _p_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Trend Over Years',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector, service=_service, fuel=_fuel)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _p_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Pie Chart',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector, service=_service, fuel=_fuel)

        elif _p_type == 'By Region':
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _p_style = {'display': 'block'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}
            _canvas = render_plot(_representation, 'By Region',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario,
                                  pattern_active=_pattern, text_active=_text, sector=_sector, service=_service,
                                  fuel=_fuel)
        else:
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _s_style = {'display': 'block'}
            _p_style = {'display': 'none'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _canvas = render_plot(_representation, 'Sankey',
                                  _data,
                                  _scenarios,
                                  _regions,
                                  _years, scenario=_scenario, sector=_sector, service=_service, fuel=_fuel)
        return _canvas, _r_style, _y_style, _fuel_style, _sector_style, _service_style, dash.no_update, _s_style, _m_style, _pattern_style, _text_style, _p_style, layers, service_value
