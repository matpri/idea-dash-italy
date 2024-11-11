import dash
from dash import Output, Input, State, ALL, dcc

from profiles.messageix_output.visualization_scripts.emissions import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'emissions'
        }, 'figure'),
        Output({
            'type': 'messageix-emissions-region-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-emissions-year-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-emissions-download',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'messageix-emissions-scenario-select',
            'index': ALL
        }, 'style'),
        Output({
            'type': 'messageix-emissions-scenario-multi-select',
            'index': ALL
        }, 'style'),
        Output(
            {
                'type': 'messageix-emissions-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        Output(
            {
                'type': 'messageix-emissions-text-switch',
                'index': ALL
            },
            'style'
        ),
        Input({
            'type': 'messageix-emissions-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-emissions-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'messageix-emissions-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-emissions-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-emissions-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'messageix-emissions-year-select',
            'index': ALL
        }, 'value'),
        Input(
            {
                'type': 'messageix-emissions-pattern-switch',
                'index': ALL
            },
            'checked'
        ),
        Input(
            {
                'type': 'messageix-emissions-text-switch',
                'index': ALL
            },
            'checked'
        ),
        Input({
            'type': 'messageix-emissions-download-button',
            'index': ALL
        }, 'n_clicks'),
        Input({
            'type': 'messageix-emissions-emission-type-select',
            'index': ALL,
        },
            'value'),
        State({
            'type': 'messageix-emissions-region-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-emissions-year-select',
            'index': ALL
        }, 'style'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'messageix_output',
            'viz': 'emissions'
        }, 'figure'),
        State({
            'type': 'messageix-emissions-download',
            'index': ALL
        }, 'data'),
        State({
            'type': 'messageix-emissions-scenario-select',
            'index': ALL
        }, 'style'),
        State({
            'type': 'messageix-emissions-scenario-multi-select',
            'index': ALL
        }, 'style'),
        State(
            {
                'type': 'messageix-emissions-pattern-switch',
                'index': ALL
            },
            'style'
        ),
        State(
            {
                'type': 'messageix-emissions-text-switch',
                'index': ALL
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_emissions(_p_type, _aggregates, _scenarios, _scenario, _regions, _years, _pattern, _text,
                         _download, _emissions_type, _r_style, _y_style, _canvas, _data, _s_style, _m_style,
                         _pattern_style, _text_style):
        print('updating emissions plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'messageix-emissions-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'messageix-emissions-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['MESSAGEix-Canada']['Emissions'].to_csv,
                                             "emissions.csv")
            return _canvas, _r_style, _y_style, _data, _s_style, _m_style, _pattern_style, _text_style

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'messageix-emissions-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        if _p_type[idx] == 'By Year':
            _m_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}

            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Year', data_handler.processed_data['MESSAGEix-Canada']['Emissions'],
                                           _aggregates[idx], _emissions_type[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        elif _p_type[idx] == 'Trend Over Years':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Trend Over Years',
                                           data_handler.processed_data['MESSAGEix-Canada']['Emissions'],
                                           _aggregates[idx], _emissions_type[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        elif _p_type[idx] == 'Pie Chart':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _text_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Pie Chart', data_handler.processed_data['MESSAGEix-Canada']['Emissions'],
                                           _aggregates[idx], _emissions_type[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])
        elif _p_type[idx] == 'Map Plot':
            _m_style[idx] = {'display': 'none'}
            _r_style[idx] = {'display': 'none'}
            _y_style[idx] = {'display': 'block'}
            _pattern_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'none'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('Map Plot', data_handler.processed_data['MESSAGEix-Canada']['Emissions'],
                                           _aggregates[idx], _emissions_type[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx])

        else:
            _m_style[idx] = {'display': 'block'}
            _y_style[idx] = {'display': 'block'}
            _r_style[idx] = {'display': 'none'}
            _s_style[idx] = {'display': 'none'}
            _pattern_style[idx] = {'display': 'block'}
            _text_style[idx] = {'display': 'block'}
            if _aggregates[idx] is not None:
                _canvas[idx] = render_plot('By Region', data_handler.processed_data['MESSAGEix-Canada']['Emissions'],
                                           _aggregates[idx], _emissions_type[idx],
                                           _scenarios[idx],
                                           _regions[idx],
                                           _years[idx], scenario=_scenario[idx],
                                           pattern_active=_pattern[idx], text_active=_text[idx])

        return _canvas, _r_style, _y_style, [dash.no_update for _ in
                                             _data], _s_style, _m_style, _pattern_style, _text_style
