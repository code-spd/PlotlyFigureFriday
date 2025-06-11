from dash_iconify import DashIconify
import dash_mantine_components as dmc
from dash import Dash, dcc, callback, Output, Input

from utils import SURVEY_REGISTRY, FIELD_TYPES, load_transform_data, prepare_bar_data


# CONSTANTS
# -----------------------------------------------------------------------------
OPACITY = 0.65
REF_LINE_COLOR = 'rgba(255, 255, 255, 0.85)'


# DATA
# -----------------------------------------------------------------------------
df = load_transform_data()

# Initial inputs
attribute = 'Age'
variable = 'Steak Preparation'
transpose = True
show_ref = False

# Initial outputs
header1 = SURVEY_REGISTRY[variable].question.replace('<br>', '')
header2 = "Broken down by respondent's " + SURVEY_REGISTRY[attribute].question.lower()

data, ref = prepare_bar_data(df, attribute, variable, transpose)
series = SURVEY_REGISTRY[variable if transpose else attribute].series_color_map(OPACITY)
ref_lines = [{'x': r, 'color': REF_LINE_COLOR} for r in ref]


# CONTENTS
# -----------------------------------------------------------------------------
slicers = dmc.Group(
    children=[
        dmc.Select(
            id='select-variable',
            label="Question topic",
            data=sorted(FIELD_TYPES['variable']),
            value=variable,
            allowDeselect=False,
            w=200,
            mb=8
        ),

        dmc.Select(
            id='select-attribute',
            label="Respondent information",
            data=sorted(FIELD_TYPES['attribute']),
            value=attribute,
            allowDeselect=False,
            w=200,
            mb=8
        ),

        dmc.Stack(
            children=[
                dmc.Checkbox(
                    id='checkbox-transpose',
                    labelPosition="right",
                    checked=transpose,
                    label="Transpose",
                    variant="filled",
                    size="sm",
                    radius="sm"
                ),

                dmc.Checkbox(
                    id='checkbox-lines',
                    labelPosition="right",
                    checked=show_ref,
                    label="Reference",
                    variant="filled",
                    size="sm",
                    radius="sm"
                )
            ],
            align='end', mb=8, ml=40, gap=18
        ),

        dmc.Space(w=20),
        
        dmc.Stack(
            children=[
                dmc.Anchor(
                    dmc.ActionIcon(
                        dmc.Avatar(
                            src="assets/Plotly-Logo-White-Short.svg",
                            radius=0,
                            size=20
                        ),
                        size="md",
                        variant="subtle",
                        n_clicks=0
                    ),
                    href="https://community.plotly.com/t/figure-friday-2025-week-23/92596",
                    target="_blank"
                ),

                dmc.Anchor(
                    dmc.ActionIcon(
                        DashIconify(icon="octicon:mark-github-16", width=20),
                        size="md",
                        variant="subtle",
                        n_clicks=0
                    ),
                    href="http://github.com/code-spd/PlotlyFigureFriday",
                    target="_blank"
                ),

            ], align='end', mb=0, pb=0, gap=6
        )
    ],
    mb=100, pl=80, justify='space-between', align='end'
)

title = dmc.Title(
    id='title-variable',
    children=header1,
    order=4,
    pl=80,
    pb=20
)

subtitles = dmc.Group(
    children=[
        dmc.Title(
            id='title-attribute',
            children=header2,
            order=6,
            pl=80
        ),
        dmc.Anchor(
            "data source: fivethirtyeight",
            href="https://github.com/fivethirtyeight/data/tree/master/steak-survey",
            target="_blank",
            size='sm',
        )
    ],
    pb=30, justify='space-between'
)

bar_chart = dmc.BarChart(
    id='bar-chart',
    h=400,
    dataKey="index",
    data=data,
    series=series,
    referenceLines=ref_lines,
    type='percent',
    orientation='vertical',
    yAxisProps={"width": 80},
    tickLine="x",
    gridAxis="y",
    withXAxis=True,
    withYAxis=True,
    withLegend=True,
    legendProps={"verticalAlign": "bottom"}
)

center_col = dmc.Stack(
    children=[
        slicers,
        title,
        subtitles,
        bar_chart
    ],
    gap=0,
    pt=40
)

main = dmc.Grid(
    children=[
        dmc.GridCol([], span=3),
        dmc.GridCol([center_col], span=6),
        dmc.GridCol([], span=3),
    ],
    gutter="xl",
)


# LAYOUT
# -----------------------------------------------------------------------------
layout = dmc.AppShell([
    dmc.AppShellMain(
        children=[
            dcc.Store(
                id='store-selections',
                data={
                    'attribute': attribute,
                    'variable': variable,
                    'transpose': transpose,
                    'show_ref': show_ref
                }
            ),
            main
        ]
    ),
])


# APP
# -----------------------------------------------------------------------------
app = Dash()
app.title = 'FigureFriday Y25W23'
app.layout = dmc.MantineProvider(
    children=layout,
    forceColorScheme="dark",
    theme = {'primaryColor': 'gray'},
)


# CALLBACKS
# -----------------------------------------------------------------------------
@callback(
    Output('store-selections', 'data'),
    Input('select-variable', 'value'),
    Input('select-attribute', 'value'),
    Input('checkbox-transpose', 'checked'),
    Input('checkbox-lines', 'checked')
)
def update_store(variable, attribute, transpose, show_ref):
    return {'attribute': attribute,
            'variable': variable,
            'transpose': transpose,
            'show_ref': show_ref}


@callback(
    Output('title-variable', 'children'),
    Output('title-attribute', 'children'),
    Output('bar-chart', 'data'),
    Output('bar-chart', 'series'),
    Output('bar-chart', 'referenceLines'),
    Input('store-selections', 'data'),
)
def update_bar_chart(store_data):
    attribute = store_data['attribute']
    variable = store_data['variable']
    transpose = store_data['transpose']
    show_ref = store_data['show_ref']

    header1 = SURVEY_REGISTRY[variable].question.replace('<br>', '')
    header2 = "Broken down by respondent's " + SURVEY_REGISTRY[attribute].question.lower()

    data, ref = prepare_bar_data(df, attribute, variable, transpose)
    series = SURVEY_REGISTRY[variable if transpose else attribute].series_color_map(OPACITY)
    ref_lines = [{'x': r, 'color': REF_LINE_COLOR} for r in ref] if show_ref else []

    return header1, header2, data, series, ref_lines


# SERVER
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=False)
