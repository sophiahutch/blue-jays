import dash
import pandas as pd
from dash import Dash, dash_table, html, Input, Output, callback, dcc
import dash_bootstrap_components as dbc


dash.register_page(__name__)

df = pd.read_csv("ML_prediction.csv")

# Layout definition
layout = html.Div([
    html.H2("Machine Learning Predictions - WAR."),
    html.Div("Writing about ML"), 
    dcc.Input(
        id='search-bar',
        type='text',
        placeholder='Search by name...'
    ),
    dash_table.DataTable(
        id='table',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['Date', 'Region']
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(220, 220, 220)',
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        }
    )
])

@callback(
    Output('table', 'data'),
    Input('search-bar', 'value')
)
def update_table(search_value):
    if search_value:
        filtered_df = df[df['Name'].str.contains(search_value, case=False, na=False)]
    else:
        filtered_df = df
    return filtered_df.to_dict('records')
    