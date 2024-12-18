import dash
from dash import Output, Input, State, MATCH, dcc, ALL

from profiles.cims_output.visualization_scripts.agriculture import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': MATCH,
            'profile': 'cims_output',
            'viz': 'agriculture'
        }, 'figure'),
        Output({
            'type': 'cims-agriculture-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-variable-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-rep_switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-rep_switch',
            'index': MATCH
        }, 'label'),
        Output({
            'type': 'cims-agriculture-pattern-switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-text-switch',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'cims-agriculture-variable-select',
            'index': MATCH
        }, 'data'), Output({
            'type': 'cims-agriculture-variable-select',
            'index': MATCH
        }, 'value'),
        Output({
            'type': 'cims-agriculture-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'cims-agriculture-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'data'),
        Output({
            'type': 'cims-agriculture-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'value'),
        Output({
            'type': 'cims-agriculture-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'style'),
        Input({
            'type': 'cims-agriculture-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-rep-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-year-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-variable-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'cims-agriculture-rep_switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-agriculture-pattern-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-agriculture-text-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'cims-agriculture-download-button',
            'index': MATCH
        }, 'n_clicks'),
        Input({
            'type': 'cims-agriculture-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'value'),
        State({
            'type': 'cims-agriculture-service-select',
            'index': MATCH,
            'layer': ALL
        }, 'style'),
        prevent_initial_call=True
    )
    def update_plot(plot_type, plot, region, year, variable, scenarios, scenario, rep_switch, pattern_switch,
                    text_switch, download_btn, _service, _service_style):
        print('Agriculture')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        _data = data_handler.processed_data['CIMS']['Agriculture']
        layers = [dash.no_update] * len(_service_style)
        service_value = _service.copy()

        if trigger_id['type'] == 'cims-agriculture-download-button':
            return (dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                    dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                    dcc.send_data_frame(_data.to_csv, "agriculture.csv")), layers, service_value, _service_style

        if 'cims-agriculture-service-select' in trigger_id['type']:
            layer = trigger_id['layer']
            layers = []
            for i in range(min(layer + 2, len(_service))):
                sub_df = _data.copy()
                for j in range(i):
                    sub_df = sub_df[sub_df['layer_{}'.format(j)] == _service[j]]
                layers.append([{'label': s, 'value': s} for s in sub_df['layer_{}'.format(i)].unique()])

            # pad layers with empty strings to make it same length as _service
            empty_layers = [[]] * (len(_service) - len(layers))
            layers.extend(empty_layers)

            # set _services to '' after layer index
            _service[layer + 1:] = [''] * len(_service[layer + 1:])

        # find first empty string in _service
        try:
            _empty = _service.index('')
        except ValueError:
            _empty = len(_service_style)

        rep_switch_label = ''

        if plot_type == 'Energy Demand':
            rep_switch_label = 'By Fuel' if rep_switch else 'By Sector'

        if plot_type == 'Emissions':
            rep_switch_label = 'By Emission' if rep_switch else 'By Sector'

        if rep_switch_label in ('By Fuel', 'By Emission'):
            if _empty > 0 and _empty < len(_service_style):
                sub_df = _data.copy()
                for i in range(_empty):
                    sub_df = sub_df[sub_df['layer_{}'.format(i)] == _service[i]]
                if len(sub_df['layer_{}'.format(_empty)].unique()) == 1:
                    _empty -= 1

            # make all _service_style block until the first empty string
            _service_style = [{'display': 'block'}] * len(_service_style)
            if _empty < len(_service_style) - 1:
                # make all _service_style none after the first empty string
                _service_style[_empty + 1:] = [{'display': 'none'}] * len(_service_style[_empty + 1:])

        else:
            _service_style = [{'display': 'none'}] * len(_service_style)

        service_value = _service.copy()
        _service = [s for s in _service if s]
        _service = '.'.join(_service) if _service else ''

        _m_style = dash.no_update
        _r_style = dash.no_update
        _y_style = dash.no_update
        _s_style = dash.no_update
        _pattern_style = dash.no_update
        _text_style = dash.no_update
        _v_style = {'display': 'none'} if plot_type == 'Energy Demand' else {'display': 'block'}

        _rep_switch_style = {'display': 'block'} if plot_type in ('Energy Demand', 'Emissions') else {'display': 'none'}

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



        df_plt = _data[_data['plot'] == plot_type]
        variables = dash.no_update
        if trigger_id['type'] == 'cims-agriculture-plot-select':
            variables = [] if plot_type == 'Energy Demand' else df_plt['parameter'].unique().tolist()
            if variables:
                variable = variables[0]
            else:
                'Energy Demand'

        _canvas = render_plot(_data, plot_type, plot, rep_switch, year, region, scenarios, scenario, variable,
                              pattern_switch, text_switch, _service)

        return (_canvas, _r_style, _y_style, _v_style, _rep_switch_style, _m_style, _s_style, rep_switch_label,
                _pattern_style, _text_style, variables, variable, dash.no_update, layers, service_value, _service_style)
