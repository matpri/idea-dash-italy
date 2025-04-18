import dash
from dash import Output, Input, State, ALL, dcc

from components import ids
from profiles.temoa_output.visualization_scripts.dispatch import render_plot, date_mapper


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Sutubra-TEMOA',
            'viz': 'Dispatch'
        }, 'figure'),
        Output({
            'type': 'temoa-dispatch-region-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'temoa-dispatch-region-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'temoa-dispatch-year-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'temoa-dispatch-year-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'temoa-dispatch-day-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'temoa-dispatch-day-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'temoa-dispatch-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'temoa-dispatch-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-dispatch-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'temoa-dispatch-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-dispatch-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-dispatch-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-dispatch-day-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'temoa-dispatch-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'temoa-dispatch-region-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'temoa-dispatch-region-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'temoa-dispatch-year-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'temoa-dispatch-year-select',
            'index': ALL
        }, 'value'),
        State({
            'type': 'temoa-dispatch-day-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'temoa-dispatch-day-select',
            'index': ALL
        }, 'value'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Sutubra-TEMOA',
            'viz': 'Dispatch'
        }, 'figure'),
        State({
            'type': 'temoa-dispatch-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True

    )
    def dispatch_callback(plot_select, aggregate_switch, scenario_multi_select, region_select, year_select, day_select,
                          download_button, region_data, region_value, year_data, year_value, day_data, day_value,
                          figure, download):
        from main import data_handler
        ctx = dash.callback_context
        #print('updating dispatch plot', ctx.triggered)
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'temoa-dispatch-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'temoa-dispatch-download-button')):
                    idx = i
                    break
            download[idx] = dcc.send_data_frame(data_handler.processed_data['Sutubra-TEMOA']['Dispatch'].to_csv,
                                                "dispatch.csv")
            return figure, region_data, region_value, year_data, year_value, day_data, day_value, download

        if 'temoa-dispatch-scenario-multi-select' in trigger_id['type']:
            df = data_handler.processed_data['Sutubra-TEMOA']['Dispatch']
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'temoa-dispatch-scenario-multi-select')):
                    idx = i
                    break

            df_scen = df.copy()
            df_scen = df_scen[df_scen['scenario'] == scenario_multi_select[idx]]
            regions = df_scen['region'].unique().tolist()
            years = df_scen['period'].unique().tolist()
            df_scen = df_scen[df_scen['period'] == years[0]]
            days = df_scen['time'].dt.strftime('%d-%m').unique().tolist()
            # sort days by month and day
            days = sorted(days, key=lambda x: (int(x.split('-')[1]), int(x.split('-')[0])))
            days = [date_mapper[int(x.split('-')[1])] + '-' + x.split('-')[0] for x in days]

            region_data[idx] = [{'label': i, 'value': i} for i in regions]
            region_value[idx] = regions[0]

            year_data[idx] = [{'label': i, 'value': i} for i in years]
            year_value[idx] = years[0]

            day_data[idx] = [{'label': i, 'value': i} for i in days]
            day_value[idx] = days[0]

            figure[idx] = render_plot(plot_select[idx], data_handler.processed_data['Sutubra-TEMOA']['Dispatch'],
                           aggregate_switch[idx], scenario_multi_select[idx], region_select[idx], year_select[idx],
                           day_select[
                               idx])

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'temoa-dispatch-plot-select')):
                idx = i
                break
        figure[idx] = render_plot(plot_select[idx], data_handler.processed_data['Sutubra-TEMOA']['Dispatch'],
                                  aggregate_switch[idx], scenario_multi_select[idx], region_select[idx],
                                  year_select[idx],
                                  day_select[
                                      idx])
        return figure, region_data, region_value, year_data, year_value, day_data, day_value, download
