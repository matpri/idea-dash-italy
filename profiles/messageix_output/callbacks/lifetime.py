import dash
from dash import Output, Input, State, MATCH, dcc, ALL

from profiles.messageix_output import utils
from profiles.messageix_output.visualization_scripts.lifetime import render_plot

from components import ids


# sources = ['Electricity', 'Gases', 'Geothermal', 'Heat', 'Liquids', 'Solids', 'Hydrogen']
# sectors = ['Electricity', 'Gases', 'Geothermal', 'Heat', 'Liquids', 'Solids', 'Hydrogen']


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'MESSAGEix-Canada',
            'viz': 'Lifetime'
        }, 'figure'),
        Output({
            'type': 'messageix-lifetime-region-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'messageix-lifetime-year-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'style'),
        Output({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'data'),
        Output({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'value'),
        Output({
            'type': 'messageix-lifetime-download',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'messageix-lifetime-scenario-select',
            'index': MATCH
        }, 'style'),
        Output({
            'type': 'messageix-lifetime-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        Output(
            {
                'type': 'messageix-lifetime-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        Output(
            {
                'type': 'messageix-lifetime-text-switch',
                'index': MATCH
            },
            'style'
        ),
        Output({
            'type': 'messageix-lifetime-show_sector-switch',
            'index': MATCH
        }, 'label'),
        Output({
            'type': 'messageix-lifetime-type-select',
            'index': MATCH
        }, 'data'),
        Output({
            'type': 'messageix-lifetime-type-select',
            'index': MATCH
        }, 'value'),
        Output({
            'type': 'messageix-lifetime-type-select',
            'index': MATCH
        }, 'label'),
        Input({
            'type': 'messageix-lifetime-plot-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-show_sector-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'messageix-lifetime-scenario-multi-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-scenario-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-region-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-year-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-type-select',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'value'),
        Input(
            {
                'type': 'messageix-lifetime-pattern-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input(
            {
                'type': 'messageix-lifetime-text-switch',
                'index': MATCH
            },
            'checked'
        ),
        Input({
            'type': 'messageix-lifetime-download-button',
            'index': MATCH
        }, 'n_clicks'),
        State({
            'type': 'messageix-lifetime-region-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'messageix-lifetime-year-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'style'),
        State({
            'type': 'messageix-lifetime-multi-level-select',
            'index': MATCH,
            'level': ALL
        }, 'data'),
        State({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'MESSAGEix-Canada',
            'viz': 'Lifetime'
        }, 'figure'),
        State({
            'type': 'messageix-lifetime-download',
            'index': MATCH
        }, 'data'),
        State({
            'type': 'messageix-lifetime-scenario-select',
            'index': MATCH
        }, 'style'),
        State({
            'type': 'messageix-lifetime-scenario-multi-select',
            'index': MATCH
        }, 'style'),
        State(
            {
                'type': 'messageix-lifetime-pattern-switch',
                'index': MATCH
            },
            'style'
        ),
        State(
            {
                'type': 'messageix-lifetime-text-switch',
                'index': MATCH
            },
            'style'
        ),
        prevent_initial_call=True
    )
    def update_lifetime(_p_type, _show_sectors, _scenarios, _scenario, _regions, _years, _types, _levels, _pattern,
                            _text,
                            _download, _r_style, _y_style, _l_style, _l_data, _canvas, _data, _s_style, _m_style,
                            _pattern_style, _text_style):
        print('updating lifetime plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        _show_sectors_label = 'Show Sector' if _show_sectors else 'Show Resource Type'
        _type_select_label = 'Sector' if _show_sectors else 'Resource Type'
        _t_data = dash.no_update
        if 'messageix-lifetime-download-button' in trigger_id['type']:

            _data = dcc.send_data_frame(data_handler.processed_data['MESSAGEix-Canada']['Lifetime'].to_csv,
                                             "lifetime.csv")
            return _canvas, _r_style, _y_style, _l_style, _l_data, _levels, _data, _s_style, _m_style, _pattern_style, _text_style, _show_sectors_label, _t_data, _types, _type_select_label
        df_scen = data_handler.processed_data['MESSAGEix-Canada']['Lifetime'].copy(deep=True)

        # df_scen = df_scen[df_scen['type'].isin(sectors)] if _show_sectors else df_scen[df_scen['type'].isin(sources)]

        if 'messageix-lifetime-type-select' in \
                trigger_id['type'] or 'messageix-lifetime-multi-level-select' in trigger_id['type'] or 'messageix-lifetime-show_sector-switch' in trigger_id['type']:

            df_scen = df_scen[(df_scen['region'] == _regions) & (df_scen['time'] == _years) & (
                    df_scen['scenario'] == _scenario)]

            if 'messageix-lifetime-show_sector-switch' in trigger_id['type']:
                _types = 'All'
                _t_data = df_scen[df_scen['type']].type.unique().tolist()
                _t_data += ['All']
                _t_data = [{'label': x, 'value': x} for x in _t_data]
            if 'messageix-lifetime-type-select' in trigger_id['type'] or 'messageix-lifetime-show_sector-switch' in trigger_id['type']:
                if _types != 'All':
                    df_scen = df_scen[df_scen['type'] == _types]

                layers = []
                styles = []

                _p = df_scen.type.unique().tolist()
                _p = ['Lifetime|' + parent for parent in _p]
                layers.append([{'label': variable, 'value': variable} for variable in _p])
                styles.append({'display': 'block'})
                for i in range(1, len(_levels)):
                    layers.append([])
                    styles.append({'display': 'none'})

                _l_data = layers
                _levels = _l_data
                _l_style = styles

        if 'messageix-lifetime-multi-level-select' in trigger_id['type']:
            interacted_level = int(trigger_id['level'])
            if not _levels[interacted_level]:
                for i in range(interacted_level + 1, len(_levels)):
                    _levels[i] = []
                    _l_style[i] = {'display': 'none'}

            else:
                parents = _levels[interacted_level]
                for i in range(interacted_level + 1, len(_levels)):
                    variable_options = df_scen[df_scen.parent.isin(parents)].variable.unique().tolist()
                    # remove all entries in levels[i] that are not in variables
                    _levels[i] = [{'label': x, 'value': x} for x in variable_options if x in _levels[i]]
                    _l_data[i] = [{'label': x, 'value': x} for x in variable_options]
                    if variable_options:
                        _l_style[i] = {'display': 'block'}
                    else:
                        _l_style[i] = {'display': 'none'}

                    parents = _levels[i]


        variables = []
        for level in _levels:
            variables.extend(level)

        parents = df_scen[df_scen.variable.isin(variables)].parent.unique().tolist()

        # remove parents from the list of variables
        variables = [x for x in variables if x not in parents]

        if _p_type== 'By Year':
            _m_style= {'display': 'block'}
            _r_style= {'display': 'block'}
            _y_style= {'display': 'none'}
            _s_style= {'display': 'none'}
            _pattern_style= {'display': 'block'}
            _text_style= {'display': 'block'}

            if _show_sectors is not None:
                _canvas= render_plot('By Year', data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario,
                                           pattern_active=_pattern, text_active=_text,
                                           variables=variables)

        elif _p_type == 'Trend Over Years by Variable':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _s_style= {'display': 'block'}

            if _show_sectors is not None:
                _canvas = render_plot('Trend Over Years by Variable',
                                           data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario, variables=variables)
        elif _p_type == 'Trend Over Years by Scenario':
            _m_style = {'display': 'block'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'none'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _s_style= {'display': 'none'}

            if _show_sectors is not None:
                _canvas = render_plot('Trend Over Years by Scenario',
                                           data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario, variables=variables)

        elif _p_type == 'Pie Chart':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _text_style = {'display': 'none'}
            _s_style= {'display': 'block'}

            if _show_sectors is not None:
                _canvas = render_plot('Pie Chart', data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario, variables=variables)

        elif _p_type == 'Map Plot':
            _m_style = {'display': 'none'}
            _r_style = {'display': 'none'}
            _y_style = {'display': 'block'}
            _pattern_style = {'display': 'none'}
            _s_style = {'display': 'block'}
            _text_style = {'display': 'none'}

            if _show_sectors is not None:
                _canvas = render_plot('Map Plot', data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario, variables=variables)

        else:
            _m_style = {'display': 'block'}
            _y_style = {'display': 'block'}
            _r_style = {'display': 'none'}
            _s_style = {'display': 'none'}
            _pattern_style = {'display': 'block'}
            _text_style = {'display': 'block'}

            if _show_sectors is not None:
                _canvas = render_plot('By Region', data_handler.processed_data['MESSAGEix-Canada']['Lifetime'],
                                           _show_sectors,
                                           _scenarios,
                                           _regions,
                                           _years, scenario=_scenario,
                                           pattern_active=_pattern, text_active=_text,
                                           variables=variables)

        return _canvas, _r_style, _y_style, _l_style, _l_data, _levels, _data, _s_style, _m_style, _pattern_style, _text_style, _show_sectors_label, _t_data, _types, _type_select_label
