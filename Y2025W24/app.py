import dash_mantine_components as dmc
from dash import Dash, dcc, callback, Output, Input, State, ctx, ALL
from dash.exceptions import PreventUpdate

from utils import VIOLATION_REGISTRY, set_custom_template_as_default

from layout.config import FONT_BODY, BACKGROUND_COLOR
from layout.header import app_header
from layout.selector import item_selector
from layout.summary import summary_section_children
from layout.visualizations import plotly_heat_map, visualization_group, legend_stack_children


set_custom_template_as_default()


# DATA
# -----------------------------------------------------------------------------
index = 0
initial_v = VIOLATION_REGISTRY[index]


# CONTENTS
# -----------------------------------------------------------------------------
center_col = dmc.Stack(
    children=[
        app_header(color='yellow'),
        dmc.Space(h=100),

        dmc.Group(
            item_selector(initial_v.label, color='yellow'),
            id='code-selector',
            justify='flex-start'
        ),
        dmc.Group(
            summary_section_children(initial_v, color='yellow'),
            id='summary-section',
            align='start',
            justify='space-between',
        ),
        dmc.Space(h=100),

        visualization_group(initial_v)
    ],
    gap=0,
    pt=0
)

main = dmc.Grid(
    children=[
        dmc.GridCol([], span=2.5),
        dmc.GridCol([center_col],span=7),
        dmc.GridCol([], span=2.5),
    ],
    gutter=0,
)


# LAYOUT
# -----------------------------------------------------------------------------
layout = dmc.AppShell([

    dmc.AppShellMain(
        children=[
            dcc.Store(id='store-selected', data={'index': index}),
            main,
        ],
        bg=BACKGROUND_COLOR
    ),
])


# APP
# -----------------------------------------------------------------------------
app = Dash(external_stylesheets=["https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&family=Montserrat+Alternates:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"])
app.title = 'FigureFriday Y25W24'
app.layout = dmc.MantineProvider(
    children=layout,
    forceColorScheme="dark",
    theme = {
        'primaryColor': 'gray',
        'fontFamily': FONT_BODY,
    },
)


# CALLBACKS
# -----------------------------------------------------------------------------
@callback(
    Output('store-selected', 'data'),
    Input({'type': 'select-code-button', 'index': ALL}, 'n_clicks'),
    Input({'type': 'increment-code-button', 'index': ALL}, 'n_clicks'),
    State('store-selected', 'data')
)
def select_code(_, __, store_data):
    triggered_id = ctx.triggered_id
    if triggered_id is None:
        raise PreventUpdate
    
    store_index = store_data['index']
    t_index = triggered_id['index']
    t_type = triggered_id['type']

    if t_type == 'increment-code-button':
        if t_index == '-':
            store_index -= 1
            store_index = len(VIOLATION_REGISTRY)-1 if store_index < 0 else store_index
        else:
            store_index += 1
            store_index = 0 if store_index >= len(VIOLATION_REGISTRY) else store_index
    else:
        store_index = int(t_index)

    new_store_data = {'index': store_index}
    return new_store_data


@callback(
    Output('code-selector', 'children'),
    Output('summary-section', 'children'),
    Output('figure-heatmap', 'figure'),
    Output('figure-waterfall', 'data'),
    Output('figure-donut', 'data'),
    Output('legend-donut', 'children'),
    Output('group-visualizations', 'style'),
    Input('store-selected', 'data'),
)
def update_data(store_data):
    v = VIOLATION_REGISTRY[store_data['index']]

    visibility = {"display": "none"} if v.total_count==0 else {"display": "flex"}
    
    return (item_selector(v.label, color='yellow'),
            summary_section_children(v, color='yellow'),
            plotly_heat_map(v),
            v.get_waterfall_data(),
            v.get_hearing_data(),
            legend_stack_children(v),
            visibility
            )

    
# SERVER
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
