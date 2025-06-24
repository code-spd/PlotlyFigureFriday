from typing import Literal

from dash_iconify import DashIconify
import dash_mantine_components as dmc

from layout.config import FONT_TITLE


# CORE ELEMENTS
def nyc_open_data_logo(color: str) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.Button(
            children=[
                dmc.Box(
                    children=[
                        dmc.Text(
                            text,
                            fw=fw,
                            c=color,
                            style={"fontSize": fs, "textAlign": "center", "letterSpacing": ls},
                            mb=mb,
                        ) 
                        for text, fs, fw, mb, ls in 
                        zip(['NYC', 'open', 'data'], [30, 26, 26],  [900, 400, 400], [-19, -18, 0], [0, 0, 1])
                    ]
                ),
            ],
            variant="light",
            color=color,
            m=0,
            p=10, pl=24, pr=24,
            h=110,
            radius=0,
        ),
        href="https://data.cityofnewyork.us/City-Government/Open-Parking-and-Camera-Violations/nc67-uf89/about_data",
        target="_blank"
    )


def title(color: str) -> dmc.Text:
    return dmc.Text(
        "2023",
        ff=FONT_TITLE,
        fw=400,
        style={"fontSize": 98, "letterSpacing": -2},
        m=0, p=0, pl=24*2, pr=12, pt=4, c=color
    )


def subtitle() -> dmc.Box:
    return dmc.Box(
        children=[
            dmc.Text(
                text,
                fw=400,
                style={"fontSize": 36, "textAlign": "left", "letterSpacing": -1},
                mb=mb,
            ) 
            for text, mb in 
            zip(['Parking and', 'Camera Violations', 'data'], [-20, -5])
        ]
    )


def link_button(label:str, href: str, img_source: str, img_type: Literal['icon', 'img'], color: str) -> dmc.Group:
    label = dmc.Text(label, fw=400, size='1.1rem', lh='1.6rem', w=100, ta='left')
    
    if img_type == 'icon':
        graphic = DashIconify(icon=img_source, width=18)
    else:
        graphic = dmc.Avatar(src=img_source, size=18, radius=0)

    action_icon = dmc.ActionIcon(
        graphic,
        size="md",
        variant="subtle",
        n_clicks=0,
        c=color,
        opacity=0.85
    )

    return dmc.Anchor(
        dmc.Group([action_icon, label], gap='xs'),
        href=href,
        target="_blank"
    )


# GROUPED ELEMENTS
def left_section(color: str) -> dmc.Group:
    return dmc.Group(
        children=[
            nyc_open_data_logo(color),
            title(color),
            subtitle(),
        ],
        align='center', justify='start', mb=-30, pb=0, gap=0
    ) 


def links_stack(color: str) -> dmc.Stack:
    links = [
        ("dmc", "https://www.dash-mantine-components.com/", "simple-icons:mantine", "icon"),
        ("plotly", "https://community.plotly.com/t/figure-friday-2025-week-24/92687", "simple-icons:plotly", "icon"),
        ("code-spd", "http://github.com/code-spd/PlotlyFigureFriday", "octicon:mark-github-16", "icon"),
    ]
    return dmc.Stack(
        children=[
            link_button(label, href, source, i_type, color)
            for label, href, source, i_type in links
        ],
        gap=2, mb=4
    )


def app_header(color: str) -> dmc.Group:
    return dmc.Group(
        children=[left_section(color), links_stack(color)],
        align='end',
        justify='space-between'
    )
