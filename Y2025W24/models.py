from collections import defaultdict
from dataclasses import dataclass, field, asdict
from typing import Any

import numpy as np


@dataclass
class Violation:
    code: int
    description: str
    definition: str = field(repr=False)
    fine_amount_manhattan_96st_and_below: list[int] = field(repr=False)
    fine_amount_all_other_areas: list[int] = field(repr=False)
    total_count: int = field(repr=False, default=0)
    total_fine: int = field(repr=False, default=0)
    total_penalty: int = field(repr=False, default=0)
    total_interest: int = field(repr=False, default=0)
    total_reduction: int = field(repr=False, default=0)
    total_payment: int = field(repr=False, default=0)
    total_due: int = field(repr=False, default=0)
    period_count: dict[str, int] = field(repr=False, default_factory=dict)
    period_fine: dict[str, int] = field(repr=False, default_factory=dict)
    statuses: dict[str, int] = field(repr=False, default_factory=dict)
    agencies: dict[str, int] = field(repr=False, default_factory=dict)
    states: dict[str, int] = field(repr=False, default_factory=dict)
    license_types: dict[str, int] = field(repr=False, default_factory=dict)
    hour_dow_counts: np.array = field(repr=False, default_factory=lambda: np.zeros((24, 7), dtype=np.int64))
    
    @property
    def hour_dow_columns(self) -> tuple[str, ...]:
        return ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
    
    @property
    def hour_dow_rows(self) -> tuple[str, ...]:
        return ('12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM',
                '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM',
                '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM',
                '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM')

    @property
    def label(self) -> str:
        if self.code==0:
            return "all codes"
        return f"code no. {self.code:0>2}"

    @property
    def fine_name_manhattan_96st_and_below(self) -> str:
        return "Manhattan ≤ 96 Street"
    
    @property
    def fine_name_all_other_areas(self) -> str:
        return "all other areas"

    @classmethod
    def from_dict(cls, data: dict) -> "Violation":
        data = data.copy()
        hour_dow_counts = np.array(
            data.pop('hour_dow_counts', np.zeros((24, 7)))
        )
        return cls(**data, hour_dow_counts=hour_dow_counts)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "hour_dow_counts": self.hour_dow_counts.tolist()
        }

    @staticmethod
    def _int_as_ordinal(n: int) -> str:
        if 10 <= (n % 100) <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"
    
    def get_fines_as_list(self, default: str = 'N/A') -> list[tuple[str, str]]:
        manhattan_fines = self.fine_amount_manhattan_96st_and_below.copy()
        all_other_fines = self.fine_amount_all_other_areas.copy()

        parsed = {}
        if manhattan_fines == all_other_fines:
            parsed['all areas'] = manhattan_fines
        else:
            parsed[self.fine_name_manhattan_96st_and_below] = manhattan_fines
            parsed[self.fine_name_all_other_areas] = all_other_fines

        output = []
        for k, v in parsed.items():
            if len(v)==1:
                output.append((k, f'${v[0]}'))
            elif len(v) > 1:
                output.append((k, f'${v[0]}-{v[-1]}'))
            else:
                output.append((k, default))
        return output
    
    def get_totals_as_list(self) -> list[tuple[str, str]]:
        return [('issued', f"{self.total_count:,.0f}"),
                ('paid', f"${self.total_payment:,.0f}"),
                ('due', f"${self.total_due:,.0f}")]

    def get_waterfall_data(self) -> list[dict]:
        return [
            {"item": "fine", "total": self.total_fine, "color": "#07bad5"},
            {"item": "penalty", "total": self.total_penalty, "color": "#B05C14"},
            {"item": "interest", "total": self.total_interest, "color": "#B05C14"},
            {"item": "reduction", "total": -self.total_reduction, "color": "#D4AE24"},
            {"item": "payment", "total": -self.total_payment, "color": "#D4AE24"},
            {"item": "due", "total": self.total_due, "color": "#07bad5", "standalone": True},
        ]
    
    def get_hearing_data(self) -> list[dict]:
        hearing_map = {'none': 'no contest',
                       'HEARING HELD-GUILTY': 'guilty',
                       'HEARING HELD-REINSTATEMENT': 'guilty',
                       'HEARING HELD-GUILTY REDUCTION': 'guilty reduced',
                       'ADMIN REDUCTION': 'guilty reduced',
                       'HEARING HELD-NOT GUILTY': 'not guilty',
                       'APPEAL AFFIRMED': 'appeal outcome',
                       'APPEAL REVERSED': 'appeal outcome',
                       'APPEAL MODIFIED': 'appeal outcome',
                       'APPEAL ABANDONED': 'appeal outcome',
                       'ADMIN CLAIM GRANTED': 'administrative review',
                       'ADMIN CLAIM DENIED': 'administrative review',
                       'HEARING ADJOURNMENT': 'pending or adjourned',
                       'HEARING PENDING': 'pending or adjourned',
                    }

        color_map = {'no contest': '#D6B527dd',
                     'guilty': '#B05C14dd',
                     'guilty reduced': '#7C2C20dd',
                     'administrative review': '#3F181Edd',
                     'not guilty': '#07bad5dd',
                     'appeal outcome': '#035E86dd',
                     'pending or adjourned': '#024764dd',
                     }

        grouped_counts = defaultdict(int)
        for status_code, count in self.statuses.items():
            group = hearing_map.get(status_code, "other outcomes")
            grouped_counts[group] += count
        
        return [{'name': key, 'value': grouped_counts[key], 'color': color}
                for key, color in color_map.items()]
