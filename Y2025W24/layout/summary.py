from typing import Literal

import dash_mantine_components as dmc

from layout.config import FONT_TITLE
from models import Violation


# CORE ELEMENTS
def violation_definition(text: str) -> dmc.Text:
    return dmc.Text(
        text,
        size='1.1rem',
        lh='1.6rem',
        mb=20
    )


def numeric_with_label(value: str, label: str, size: Literal['sm', 'lg'], color: str) -> dmc.Group:
    value_size = '1.4rem' if size=='sm' else '2.0rem'
    label_size = '1.1rem' if size=='sm' else '1.2rem'
    label_width = None if size=='sm' else 100
    label_margin_bottom = 2 if size=='sm' else 4

    return dmc.Group(
        children=[
            dmc.Text(
                value,
                c=color,
                size=value_size,
                ff=FONT_TITLE,
                span=True
            ),
            dmc.Text(
                f" {label}",
                size=label_size,
                span=True,
                w=label_width,
                mb=label_margin_bottom
            ),
        ],
        gap='xs',
        align='end',
    )


# GROUPED ELEMENTS
def fine_amounts(v: Violation, color: str) -> dmc.Group:
    return dmc.Group(
        children=[
            numeric_with_label(value, label, 'sm', color)
            for label, value in v.get_fines_as_list()
        ],
        gap='lg',
    )


def left_section(v: Violation, color:str) -> dmc.ScrollArea:
    return dmc.ScrollArea(
        children=[
            violation_definition(v.definition),
            fine_amounts(v, color),
        ],
        type='auto',
        scrollbarSize=16,
        h=122, w=670,
        m=0, p=0
    )


def right_section(v: Violation, color: str) -> dmc.Stack:
    return dmc.Stack(
        children=[
            numeric_with_label(value, label, 'lg', color)
            for label, value in v.get_totals_as_list()
        ],
       justify='end', align='end', mt=0, gap=6
    )


def summary_section_children(v: Violation, color: str) -> list:
    return [
        left_section(v, color),
        right_section(v, color)
    ]
