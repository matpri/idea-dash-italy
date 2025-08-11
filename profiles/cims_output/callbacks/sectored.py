import dash
from dash import Output, Input, State, MATCH, dcc, ALL

from profiles.cims_output.visualization_scripts.sectored import render_plot

def create_link(sector):
    lower_sector = sector.lower()
    lower_sector = lower_sector.replace(' ', '_')
    def link(app):
        @app.callback(
            Output({
                'type': 'figure',
                'index': MATCH,
                'profile': 'CIMS',
                'viz': sector
            }, 'figure'),
            Output({
                'type': f'cims-{lower_sector}-region-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-year-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-variable-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-rep_switch',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-scenario-multi-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-scenario-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-rep_switch',
                'index': MATCH
            }, 'label'),
            Output({
                'type': f'cims-{lower_sector}-pattern-switch',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-text-switch',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-variable-select',
                'index': MATCH
            }, 'data'), Output({
                'type': f'cims-{lower_sector}-variable-select',
                'index': MATCH
            }, 'value'),
            Output({
                'type': f'cims-{lower_sector}-download',
                'index': MATCH
            }, 'data'),
            Output({
                'type': f'cims-{lower_sector}-service-select',
                'index': MATCH,
                'layer': ALL
            }, 'data'),
            Output({
                'type': f'cims-{lower_sector}-service-select',
                'index': MATCH,
                'layer': ALL
            }, 'value'),
            Output({
                'type': f'cims-{lower_sector}-service-select',
                'index': MATCH,
                'layer': ALL
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-rep-select',
                'index': MATCH,
            }, 'data'),
            Output({
                'type': f'cims-{lower_sector}-rep-select',
                'index': MATCH,
            }, 'value'),
            Output({
                'type': f'cims-{lower_sector}-energy-rep-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-emissions-rep-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-tech-service-select',
                'index': MATCH
            }, 'style'),
            Output({
                'type': f'cims-{lower_sector}-tech-service-select',
                'index': MATCH
            }, 'data'),
            Input({
                'type': f'cims-{lower_sector}-plot-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-rep-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-region-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-year-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-variable-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-scenario-multi-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-scenario-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-rep_switch',
                'index': MATCH
            }, 'checked'),
            Input({
                'type': f'cims-{lower_sector}-pattern-switch',
                'index': MATCH
            }, 'checked'),
            Input({
                'type': f'cims-{lower_sector}-text-switch',
                'index': MATCH
            }, 'checked'),
            Input({
                'type': f'cims-{lower_sector}-download-button',
                'index': MATCH
            }, 'n_clicks'),
            Input({
                'type': f'cims-{lower_sector}-service-select',
                'index': MATCH,
                'layer': ALL
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-energy-rep-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-emissions-rep-select',
                'index': MATCH
            }, 'value'),
            Input({
                'type': f'cims-{lower_sector}-tech-service-select',
                'index': MATCH
            }, 'value'),
            State({
                'type': f'cims-{lower_sector}-service-select',
                'index': MATCH,
                'layer': ALL
            }, 'style'),
            prevent_initial_call=True
        )
        def update_plot(plot_type, plot, region, year, variable, scenarios, scenario, rep_switch, pattern_switch,
                        text_switch, download_btn, _service, energy_rep, emissions_rep, tech_service, _service_style):
            print(sector)
            from utils.data_state import data_handler
            ctx = dash.callback_context
            trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
            _data = data_handler.processed_data['CIMS'][sector]
            layers = [dash.no_update] * len(_service_style)
            service_value = _service.copy()
    
            if trigger_id['type'] == f'cims-{lower_sector}-download-button':
                return (dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                        dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
                        dcc.send_data_frame(_data.to_csv, f"{lower_sector}.csv")), layers, service_value, _service_style, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
            if f'cims-{lower_sector}-service-select' in trigger_id['type']:
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
    
            # Handle Technology Stocks - use current sector tab name and filter services accordingly
            tech_services = dash.no_update
            if plot_type == 'Technology Stocks':
                current_sector = sector
                tech_data = _data[_data['plot'] == 'Technology Stocks']
                tech_data = tech_data[tech_data['sector'] == current_sector]
                tech_services = tech_data[tech_data['technology'].notna()]['short_path'].unique().tolist()
    
            # find first empty string in _service
            try:
                _empty = _service.index('')
            except ValueError:
                _empty = len(_service_style)
    
            rep_switch_label = ''
            
            if plot_type == 'Energy Demand':
                rep_switch = (energy_rep == 'By Fuel')
                rep_switch_label = energy_rep if energy_rep else 'By Service'
    

            if plot_type == 'Emissions':
                rep_switch = (emissions_rep == 'By Emission')
                rep_switch_label = emissions_rep if emissions_rep else 'By Service'
    
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

            _rep_options = [{'label': plot, 'value': plot} for plot in ['Sankey', 'Trend Over Years']] if rep_switch_label == 'By Service' else [{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']]

            if trigger_id['type'] == f'cims-{lower_sector}-plot-select' or trigger_id['type'] == f'cims-{lower_sector}-energy-rep-select' or trigger_id['type'] == f'cims-{lower_sector}-emissions-rep-select':
                plot = 'Sankey' if rep_switch_label == 'By Service' else 'By Year'
    
            # Modified to show representation dropdowns for Energy Demand and Emissions, hide toggle for Technology Stocks
            _rep_switch_style = {'display': 'none'} if plot_type in ('Energy Demand', 'Emissions', 'Technology Stocks') else {'display': 'block'}
            _energy_rep_style = {'display': 'block'} if plot_type == 'Energy Demand' else {'display': 'none'}
            _emissions_rep_style = {'display': 'block'} if plot_type == 'Emissions' else {'display': 'none'}
            _tech_service_style = {'display': 'block'} if plot_type == 'Technology Stocks' else {'display': 'none'}
    
            if plot == 'By Year':
                _m_style = {'display': 'block'}
                _r_style = {'display': 'block'}
                _y_style = {'display': 'none'}
                _s_style = {'display': 'none'}
                _pattern_style = {'display': 'block'}
                _text_style = {'display': 'block'}
            elif plot == 'Trend Over Years' or plot == 'Sankey':
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
            if trigger_id['type'] == f'cims-{lower_sector}-plot-select':
                variables = [] if plot_type == 'Energy Demand' else df_plt['parameter'].unique().tolist()
                if variables:
                    variable = variables[0]
                else:
                    variable = 'Energy Demand'
    
            _canvas = render_plot(sector,_data, plot_type, plot, rep_switch, year, region, scenarios, scenario, variable,
                                  pattern_switch, text_switch, _service, sector, tech_service)
    
            return (_canvas, _r_style, _y_style, _v_style, _rep_switch_style, _m_style, _s_style, rep_switch_label,
                    _pattern_style, _text_style, variables, variable, dash.no_update, layers, service_value, _service_style,
                    _rep_options, plot, _energy_rep_style, _emissions_rep_style, _tech_service_style, tech_services)

    return link