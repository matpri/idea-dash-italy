from dash import Input, Output, State, ALL, callback_context, MATCH
from components import ids

def link(app):
    app.callback(
        Output({'type': ids.PLOT, 'index': MATCH}, 'figure'),
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
        }, 'figure'),Input({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': ALL,
            'name': ALL
        }, 'figure'),
        State({'type': ids.PLOT, 'index': MATCH}, 'figure'),
        prevent_initial_call=True,
    )(update_plot)


def update_plot(_figs, _figs2, _fig3, _fig4, _plots):
    """
    Update the plot based on the triggered input.
    These are all id structures that are used to identify plots in IDEA (COULD BE UNIFIED TO ONE ID STRUCTURE) and when a plot is updated, we need to update the plots inside the tabs.
    This is done as we need to wrap the figure for the plots' sizes to acurately update on resize.
    """
    ctx = callback_context

    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]['value']
    return triggered_value
