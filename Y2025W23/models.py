class ColorScheme:
    """Store RGB color schemes with method to convert to RGBA"""
    def __init__(self, rgb: list[str]):
        self.rgb: list[str] = rgb

    def __repr__(self):
        return f"ColorScheme(rgb=[{', '.join(self.rgb)}])"

    @staticmethod
    def _convert_rgb_to_rgba(rgb: str, a: float) -> str:
        r, g, b = rgb[4:-1].split(', ')
        return f"rgba({r}, {g}, {b}, {a})"

    def as_rgba(self, a: float) -> list[str]:
        return [self._convert_rgb_to_rgba(c, a) for c in self.rgb]
    

class SurveyField:
    """
    Essentially a dataclass to bundle information for each column/question in the survey.
    Makes it easier to rename columns, convert to categorical data types with preferred 
    ordering (see https://pandas.pydata.org/docs/user_guide/categorical.html), assign 
    color schemes, and differentiate between between respondent characteristics 
    (i.e., attributes) and the survey questions (i.e., variables).
    """
    def __init__(self, name: str, question: str, responses: str, field_type: str, colors: ColorScheme):
        self.name: str = name  # Concise new column name
        self.question: str = question  # Original column name from source
        self.responses: list[str] = responses  # Categorical values with preferred ordering
        self.field_type: str = field_type  # Differentiate fields by type
        self.colors: ColorScheme = colors  # Colors to use in visualizations

    def __repr__(self):
        return f"SurveyField(name={self.name!r}, num_responses={len(self.responses)})"

    def color_map(self, a: float | None = None) -> dict[str, str]:
        colors = self.colors.as_rgba(a) if a else self.colors.rgb
        return dict(zip(self.responses, colors))
    
    def series_color_map(self, a: float | None = None) -> list[dict]:
        return [{"name": k, "color": c} for k, c in self.color_map(a).items()]
