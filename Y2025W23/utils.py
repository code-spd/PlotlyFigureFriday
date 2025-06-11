import pandas as pd

from models import ColorScheme, SurveyField


# Define colors and survey field information here to make `app.py` less cluttered
BINARY_COLOR = ColorScheme(['rgb(229, 56, 59)', 'rgb(245, 243, 244)'])
STEAK_COLOR = ColorScheme(['rgb(164, 22, 26)', 'rgb(229, 56, 59)', 'rgb(192, 165, 164)', 'rgb(211, 211, 211)', 'rgb(245, 243, 244)'])
GENDER_COLOR = ColorScheme(['rgb(114, 1, 168)', 'rgb(31, 158, 137)'])
AGE_COLOR = ColorScheme(['rbg(217, 237, 146)', 'rbg(153, 217, 140)', 'rbg(82, 182, 154)', 'rbg(22, 138, 173)'])
INCOME_COLOR = ColorScheme(['rgb(255, 192, 62)', 'rgb(233, 174, 42)', 'rgb(189, 147, 43)', 'rgb(136, 114, 53)', 'rgb(92, 83, 55)'][::-1])
EDUCATION_COLOR = ColorScheme(['rgb(90, 13, 109)', 'rgb(131, 44, 115)', 'rgb(172, 73, 121)', 'rgb(213, 103, 127)', 'rgb(255, 134, 134)'][::-1])
LOCATION_COLOR = ColorScheme(['rbg(96, 73, 90)', 'rbg(167, 90, 90)', 'rbg(125, 186, 96)', 'rbg(194, 209, 27)', 'rbg(246, 153, 45)', 'rbg(255, 200, 0)', 'rbg(12, 99, 127)', 'rbg(76, 118, 128)', 'rbg(56, 163, 165)'])

SURVEY_FIELDS =[
    SurveyField(name='Lottery',
                question='Consider the following hypothetical situations: <br>In Lottery A, you have a 50% chance of success, with a payout of $100. <br>In Lottery B, you have a 90% chance of success, with a payout of $20. <br><br>Assuming you have $10 to bet, would you play Lottery A or Lottery B?',
                responses=['Lottery A', 'Lottery B'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Cigarettes',
                question='Do you ever smoke cigarettes?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Alcohol',
                question='Do you ever drink alcohol?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Gamble',
                question='Do you ever gamble?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Skydived',
                question='Have you ever been skydiving?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Speed',
                question='Do you ever drive above the speed limit?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Cheated',
                question='Have you ever cheated on your significant other?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Steak',
                question='Do you eat steak?',
                responses=['Yes', 'No'],
                field_type='variable',
                colors=BINARY_COLOR),

    SurveyField(name='Steak Preparation',
                question='How do you like your steak prepared?',
                responses=['Rare', 'Medium rare', 'Medium', 'Medium Well', 'Well'],
                field_type='variable',
                colors=STEAK_COLOR),

    SurveyField(name='Gender',
                question='Gender',
                responses=['Female', 'Male'],
                field_type='attribute',
                colors=GENDER_COLOR),

    SurveyField(name='Age',
                question='Age',
                responses=['18-29', '30-44', '45-60', '> 60'],
                field_type='attribute',
                colors=AGE_COLOR),

    SurveyField(name='Income',
                question='Household Income',
                responses=['$0 - $24,999',
                           '$25,000 - $49,999',
                           '$50,000 - $99,999',
                           '$100,000 - $149,999',
                           '$150,000+'],
                field_type='attribute',
                colors=INCOME_COLOR),

    SurveyField(name='Education',
                question='Education',
                responses=['Less than high school degree',
                           'High school degree', 
                           'Some college or Associate degree',
                           'Bachelor degree',
                           'Graduate degree'],
                field_type='attribute',
                colors=EDUCATION_COLOR),
                
    SurveyField(name='Location',
                question='Location (Census Region)',
                responses=['Pacific',
                           'Mountain',
                           'West North Central',
                           'East North Central',
                           'West South Central',
                           'East South Central',
                           'New England',
                           'Middle Atlantic',
                           'South Atlantic'],
                field_type='attribute',
                colors=LOCATION_COLOR)
]

# Quick access to survey field information
# Makes it easy to convert selection from `dmc.Select` to the original survey question or its color scheme
SURVEY_REGISTRY = {f.name: f for f in SURVEY_FIELDS}

FIELD_TYPES = {'attribute': [f.name for f in SURVEY_FIELDS if f.field_type=='attribute'],
               'variable': [f.name for f in SURVEY_FIELDS if f.field_type=='variable']}


def load_transform_data(filepath: str = 'Y2025W23/steak-risk-survey.csv',
                        registry: dict[str, SurveyField] = SURVEY_REGISTRY) -> pd.DataFrame:
    """
    Loads source data, renames columns, and converts to categorical data types.
    See https://pandas.pydata.org/docs/user_guide/categorical.html for more information.
    """
    dataframe = pd.read_csv(filepath).set_index('RespondentID')
    dataframe.rename(columns={f.question: name for name, f in registry.items()},
                     inplace=True)

    for col, field in registry.items():
        dataframe[col] = pd.Categorical(dataframe[col], categories=field.responses, ordered=True)

    return dataframe


def prepare_bar_data(dataframe: pd.DataFrame,
                     attribute: str,
                     variable: str,
                     transpose: bool = False) -> tuple[list, list]:
    """
    Generates input for `data` prop in `dmc.BarChart` as-is. Also calculates
    percent x-values that can be used to generate input for `referenceLines`.
    """
    x = variable if transpose else attribute
    y = attribute if transpose else variable

    group = [x, y]

    dff = dataframe[group].copy()
    dff['value'] = 1
    dff = dff.groupby(group, observed=True).sum().reset_index()
    dff = dff.pivot(index=y, columns=x, values='value')

    # Add totals for all respondents
    dff = pd.concat([dff,
                     pd.DataFrame(index=['All'], data=[{col: dff[col].sum() for col in dff}])])

    data = dff.reset_index().to_dict('records')

    # Determine x-values as percent for reference lines
    dff_ref = dff.loc['All'].to_frame()
    dff_ref['csum'] = dff_ref['All'].cumsum()
    dff_ref['perc'] = dff_ref['csum'] / dff_ref['All'].sum()

    ref = dff_ref['perc'].iloc[:-1].values.tolist()
    return data, ref
