from typing import Literal

from dash_iconify import DashIconify
import dash_mantine_components as dmc

from layout.config import BACKGROUND_COLOR
from utils import VIOLATION_REGISTRY


# CORE ELEMENTS
def increment_button(button_id: str, direction: Literal['+', '-'], color: str) -> dmc.ActionIcon:
    icon = "mingcute:left-line" if direction=='-' else "mingcute:right-line"

    return dmc.ActionIcon(
        DashIconify(icon=icon, width=32),
        id=button_id,
        variant="light",
        color=color,
        m=0,
        p=0,
        w=40,
        h=40,
        radius=0
    )


def select_menu(label: str, text_id: str, button_id: str, color: str) -> dmc.Menu:
    target = dmc.Button(
        children=[
            dmc.Text(
                label,
                id=text_id,
                c=color,
                fw=400,
                style={"fontSize": 30, "textAlign": "left", "letterSpacing": 0},
                mb=0,
            )
        ],
        variant="light",
        color=color,
        m=0,
        p=4,
        h=40,
        radius=0,
        w=200
    )

    menu_items = [
        dmc.MenuItem(
            dmc.Group([
                dmc.Text(f"{v.code:0>2}", w=22),
                dmc.Text(v.description.title(), w=300),
                dmc.Text(f"{v.total_count:,.0f}", ta='right', w=100),
            ]),
            id={'type': 'select-code-button', 'index': i},
            n_clicks=0,
        )
        for i, v in enumerate(VIOLATION_REGISTRY)
    ]

    drop_down = dmc.ScrollArea(
        children=menu_items,
        type="hover",
        scrollbarSize=16,
        scrollHideDelay=1000,
        offsetScrollbars=True,
        h=380,
    )

    return dmc.Menu(
        children=[
            dmc.MenuTarget(target),
            dmc.MenuDropdown(drop_down, bg=BACKGROUND_COLOR)
        ]
    )


# GROUPED ELEMENTS
def item_selector(label: str,
                  color: str,
                  text_id: str = 'selector-center-text',
                  center_id: str = 'selector-center-button',
                  left_id: str | dict = {'type': 'increment-code-button', 'index': '-'},
                  right_id: str | dict = {'type': 'increment-code-button', 'index': '+'}
                  ) -> dmc.Group:
    return dmc.Group(
        children=[
            increment_button(left_id, '-', color),
            select_menu(label, text_id, center_id, color),
            increment_button(right_id, '+', color),
        ],
        gap=0,
        mb=10,
        align='start', justify='space-between'
    )
