
import json
from pathlib import Path

from models import Violation
from layout.config import FONT_BODY


# Data preparation
DATA_DIR = Path('data')
with open(DATA_DIR / 'nyc_parking_violation_data.json', 'r', encoding='utf-8') as fp:
    violation_data = json.load(fp)


VIOLATION_REGISTRY = [Violation.from_dict(v) for v in violation_data]


def set_custom_template_as_default() -> None:
    import plotly.io as pio
    # Figure templates
    custom = dict(
        layout=dict(
            margin=dict(pad=5, t=0, l=50, r=50, b=50),
            font=dict(family=FONT_BODY, size=12, color="#828282"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, showline=False),
            yaxis=dict(showgrid=False, zeroline=False, showline=False),
        )
    )
    pio.templates['custom'] = custom
    pio.templates.default = 'custom'


def format_number_si(value: float) -> str:
    abs_value = abs(value)

    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.3g}B"
    elif abs_value >= 1_000_000:
        return f"{value / 1_000_000:.3g}M"
    elif abs_value >= 1_000:
        return f"{value / 1_000:.3g}K"
    else:
        return str(int(value)) if value == int(value) else str(value)
