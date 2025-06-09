import dash
from dash import Input, Output, State, ALL, callback_context, MATCH, dcc
from components import ids

def link(app):
    app.callback(
        Output({'type': ids.PLOT, 'index': MATCH}, 'figure'),
        Output({'type': ids.PLOT, 'index': MATCH}, 'style'),
        Output({'type': 'MD', 'index': MATCH}, 'children'),
        Output({'type': 'MD', 'index': MATCH}, 'style'),
        Output({'type': ids.BURGER, 'index': MATCH}, 'style'),
        Output({'type': ids.DRAWER, 'index': MATCH}, 'style'),
        Input({'type': ids.FIGURE, 'index': MATCH,
               'profile': ALL, 'viz': ALL}, 'figure'),
        Input({
            'type': ids.FIGURE,
            'index': MATCH,
            'model': ALL,
            'name': ALL
        }, 'figure'),
        Input({
            'type': ids.FIGURE,
            'index': MATCH,
            'model': ALL,
            'viz': ALL
        }, 'figure'),
        Input({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': ALL,
            'name': ALL
        }, 'figure'),
        Input({
            'type': 'markdown',
            'index': MATCH,
            'profile': ALL,
        },
            'children'),
        State({'type': ids.PLOT, 'index': MATCH}, 'figure'),
        prevent_initial_call=True,
    )(update_plot)


def update_plot(_figs, _figs2, _fig3, _fig4, _md1, _plots):
    """
    Update the plot based on the triggered input.
    These are all id structures that are used to identify plots in IDEA (COULD BE UNIFIED TO ONE ID STRUCTURE) and when a plot is updated, we need to update the plots inside the tabs.
    This is done as we need to wrap the figure for the plots' sizes to acurately update on resize.
    """
    from utils.data_state import data_handler
    ctx = callback_context

    triggered_id = ctx.triggered_id
    if triggered_id is None:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    triggered_value = ctx.triggered[0]['value']
    if triggered_id['type'] == ids.FIGURE:
        profile = triggered_id.get('profile', None)
        if profile is None:
            profile = triggered_id['model']
        viz = triggered_id.get('viz', None)
        if viz is None:
            viz = triggered_id['name']
        desc = None
        for _, report in data_handler.reports.items():
            if profile in report.descriptions:
                desc = report.descriptions[profile].get(viz, None)

        # update plot title with a sub heading with description
        if desc is not None:
            try:
                title = triggered_value['layout']['title']['text']
            except:
                title = ''

            if desc not in title:
                triggered_value['layout']['title']['text'] = title + f"<br><sub>{desc}</sub>"

        return triggered_value, {
            'width': '100%',
            'height': '100%',
            'display': 'block',
        }, dash.no_update, {'width': '0%', 'height': '0%', 'display': 'none'}, {'display': 'block'}, {'width': '20%','height': '100%'}

    else:
        return dash.no_update, {
            'width': '0%',
            'height': '0%',
            'display': 'none',
        }, dcc.Markdown(triggered_value), {'width': '100%', 'height': '100%', 'display': 'block', 'overflow': 'auto'}, {'opacity': '0', 'visibility': 'hidden'}, {'display': 'none'}
