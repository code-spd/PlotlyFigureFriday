from dash import dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import plotly.graph_objects as go

from models import Violation
from utils import format_number_si


# CORE ELEMENTS
def figure_title(lines: list[str]) -> list[dmc.Text]:
    return [
        dmc.Text(
            label,
            size='1.2rem',
            ta='left'
        )
        for label in lines
    ]


def legend_item(color: str, label: str, value: int | float) -> dmc.Group:
    return dmc.Group(
        children=[
            dmc.Text(
                DashIconify(icon="material-symbols:circle", width=14, color=color),
                mt=5, ml=-6
            ),
            dmc.Text(format_number_si(value), size='0.7rem', ta='right', w=34),
            dmc.Text(label, size='0.7rem', ta='left', w=100, c="#828282"),
        ],
        gap='xs', align='center', justify='end', mb=0
    )


def plotly_heat_map(v: Violation) -> go.Figure:
    colors = ['rgba(39, 17, 23, 0.7)', 'rgba(51, 19, 23, 0.75)', 'rgba(79, 28, 33, 0.8)', 'rgba(108, 36, 36, 0.85)', 'rgba(135, 47, 32, 0.9)', 'rgba(157, 66, 25, 0.95)', 'rgba(174, 88, 20, 1)', 'rgba(188, 111, 19, 1)', 'rgba(199, 137, 22, 1)', 'rgba(209, 164, 32, 1)', 'rgba(217, 192, 44, 1)', 'rgba(222, 222, 59, 1)', 'rgba(224, 253, 74, 1)']

    x = [c[0].lower() if c[0] not in ['S', 'T'] else c[:2].lower() for c in v.hour_dow_columns]
    y = [h.lower() for h in v.hour_dow_rows]
    z = v.hour_dow_counts

    fig = go.Figure(go.Heatmap(
        x=x,
        y=y,
        z=z,
        colorscale=colors,
        zmin=0,
        zmax=1 if z.max()==1 else z.max(),
        hoverongaps=False,
        showscale=False,
        xgap=3.5,
        ygap=3.5,
    ))

    fig.update_layout(
        margin=dict(pad=2, b=50, t=0),
        dragmode=False,
        xaxis=dict(
            tickvals=x[1::2],
            side='bottom',
            showgrid=False,
            showline=False,
            zeroline=False,
            ticklen=0
        ),
        yaxis=dict(
            autorange='reversed',
            tick0=12,
            dtick=6,
            tickvals=y[6::6],
            showgrid=False,
            showline=False,
            zeroline=False,
            ticklen=0,
            side='right'
        )
    )
    return fig


def dmc_waterfall(v: Violation, waterfall_id: str) -> dmc.BarChart:
    return dmc.BarChart(
        h=370,
        w=550,
        id=waterfall_id,
        data=v.get_waterfall_data(),
        dataKey="item",
        type="waterfall",
        series=[{'name': 'total'}],
        withLegend=False,
        barProps={"radius": 5, "isAnimationActive": True},
        withYAxis=True,
        yAxisProps={"orientation": "right", "padding": {"left": 30, "right": 30}},
        tickLine="none",
        valueFormatter={"function": "formatNumberIntl"},
        fillOpacity=0.8,
        tooltipAnimationDuration=200,
    )


def dmc_donut(v: Violation, donut_id: str) -> dmc.DonutChart:
    return dmc.DonutChart(
        id=donut_id,
        data=v.get_hearing_data(),
        withTooltip=False,
        pieProps={"isAnimationActive": True, "animationDuration": 1_000, "animationBegin": 100},
        paddingAngle=2
    )


# GROUPED ELEMENTS
def heat_map_stack(v: Violation, heatmap_id: str = 'figure-heatmap') -> dmc.Stack:
    return dmc.Stack(
        children=[
            dmc.Box(
                figure_title(['no. violations', 'by time issued']),
                ml=28
            ),
            dcc.Graph(
                figure=plotly_heat_map(v),
                id=heatmap_id,
                style={'height': 400, 'width': 210, "align": "center"},
                config={'displayModeBar': False}
            )
        ],
        ml=-26
    )


def waterfall_stack(v: Violation, waterfall_id: str = 'figure-waterfall') -> dmc.Stack:
    return dmc.Stack(
        children=[
            dmc.Box(
                figure_title(['fine and', 'payment details']),
                ml=8
            ),
            dmc_waterfall(v, waterfall_id)
        ]
    )


def legend_stack_children(v: Violation) -> list:
    data = v.get_hearing_data()
    return [legend_item(d['color'], d['name'], d['value'])
            for d in data]


def donut_stack(v: Violation, donut_id: str = 'figure-donut', legend_id: str = 'legend-donut') -> dmc.Stack:
    return dmc.Stack(
        children=[
            dmc.Box(
                figure_title(['hearing and', 'appeal outcomes']),
                ml=0
            ),
            dmc_donut(v, donut_id),
            dmc.Stack(legend_stack_children(v), id=legend_id, gap=0)
        ]
    )


def visualization_group(v: Violation, group_id: str = 'group-visualizations') -> dmc.Group:
    return dmc.Group(
        children=[
            heat_map_stack(v),
            waterfall_stack(v),
            donut_stack(v)
        ],
        id=group_id,
        align='start', justify='space-between',
        style={"display": "flex"}
    )
