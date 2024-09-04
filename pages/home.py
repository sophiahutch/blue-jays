from dash import callback, Output, Input, dcc, Dash, html, State
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Container import Container
import pandas as pd
import dash_gif_component as gif
from datetime import date, datetime
import requests
import time
import statsapi


dash.register_page(__name__, path='/')

BLUEJAYS_LOGO = '/assets/batflip.png'
GIF_JAYS = '/assets/toronto-blue-jays-ace.gif'

today = datetime.today().strftime('%Y-%m-%d')

games = statsapi.schedule(start_date=today, end_date='', team='', opponent='', sportId=1,game_id=None)
G= pd.json_normalize(games)
df = pd.DataFrame(G)



def game_day_summary(G):
    if G.loc[G['home_name'] == 'Toronto Blue Jays'].empty and G.loc[G['away_name'] == 'Toronto Blue Jays'].empty:
        return "The Blue jays are not playing today."
    elif not G.loc[G['home_name'] == 'Toronto Blue Jays'].empty:
        return G.loc[G['home_name'] == 'Toronto Blue Jays', 'summary'].values[0]
    else:
        return G.loc[G['away_name'] == 'Toronto Blue Jays', 'summary'].values[0]

def check_for_home(df):
    return 'Toronto Blue Jays' in df['home_name'].values[0]
def check_for_away(df):
    return 'Toronto Blue Jays' in df['away_name'].values[0]


toronto_row = df[(df['away_name'] == 'Toronto Blue Jays') | (df['home_name'] == 'Toronto Blue Jays')] 


def innings_check(df):
    if toronto_row['status'].values[0]== "Pre-Game":
        return 'Pre-Game'
    elif toronto_row['status'].values[0]== "In Progress" and toronto_row['inning_state'].values[0] == 'Top':
        return 'Top'
    elif toronto_row['status'].values[0]== "In Progress" and toronto_row['inning_state'].values[0] == 'Bottom':
        return 'Bottom'
    elif toronto_row['status'].values[0]== "Final":
        return 'Final'
pitch_home=''
pitch_away=''
def team_W_L_check(df):
    if toronto_row['winning_team'].values[0] == toronto_row['away_name'].values[0]:
        pitch_away = toronto_row['winning_pitcher'].values[0]
        return pitch_away
    elif toronto_row['losing_team'].values[0] == toronto_row['away_name'].values[0]:
        pitch_away = toronto_row['losing_pitcher'].values[0]
        return pitch_away
    elif toronto_row['losing_team'].values[0] == toronto_row['home_name'].values[0]:
        pitch_home = toronto_row['losing_pitcher'].values[0]
        return pitch_home
    elif toronto_row['winning_team'].values[0] == toronto_row['home_name'].values[0]:
        pitch_home = toronto_row['winning_pitcher'].values[0]
        return pitch_home

def game_summary(toronto_row):
    if toronto_row['status'].values[0] != "In Progress":
        return dbc.Container([
            html.H4("The Toronto Blue Jays game has not started yet."),
            html.H6("Check back later for batting and pitching updates!"),
            # html.Div(gif.GifPlayer("/assets/giphy.gif"), still='assets/jayspic.jpg',)
        ])
    else:
        new_g = statsapi.boxscore(toronto_row["game_id"].values[0],battingBox=True, battingInfo=True, fieldingInfo=True, pitchingBox=True, gameInfo=True, timecode=None)
        return dbc.Container([
    html.Pre(new_g
                 , style={
        'whiteSpace': 'pre-wrap',
        'fontFamily': 'Courier, monospace',
        'fontSize': '14px',
        'border': '1px solid black',
        'padding': '10px',
        'backgroundColor': '#f7f7f7',
        'overflowX': 'auto'
    }
    )
    ])

layout = html.Div([
        html.Br(),
        html.H1("Today\'s schedule - " + today),
        dbc.Row([
            dbc.Col([
            dbc.Container([
            dbc.Row([
                html.Div(
                children =[ 
                dbc.Col([
                    html.H3(toronto_row['away_name']),
                ],width={"size":"auto"},
                ),
                dbc.Col([
                    html.H3("@"),

                    ], 
                       width={"size":"auto"}, 
                       align='center'),
                dbc.Col([
                    html.H3(toronto_row['home_name']),

                    ],width={"size":"auto"},)
            ],style={
                'display': 'flex',
                'justify-content': 'space-between',
                'width': '100%'}
            ),
        dbc.Row([
            html.Div(children=[
                dbc.Col([
                    html.H4(toronto_row['away_score']),

                    ], width={"size":"auto"},),
                dbc.Col([
                    innings_check(df),

                    ], width={'size':'auto'}),
                dbc.Col([
                    html.H4(toronto_row['home_score']), 
                     ], width={"size":"auto"},), 
             ],style={
                'display': 'inline-flex',
                'justify-content': 'space-between',
                'width': '100%',
                'margin-left': '10px',
                'margin-right':'10px'
                }
            )
            ]),
            dbc.Row([
                html.Div("Pitchers")
                ]),
            dbc.Row([
                html.Div(children=[
                    dbc.Col([
                        html.H6(toronto_row['away_probable_pitcher'].values)
                        ], width={'size':'auto'}),
                    dbc.Col([
                        html.H6(toronto_row['home_probable_pitcher'].values)
                        ], width={'size':'auto'})
            ],style={
                'display': 'inline-flex',
                'justify-content': 'space-between',
                'width': '100%',
                'margin-left': '10px',
                'margin-right':'10px'
                }) 
                if toronto_row['status'].values[0]!='Final' else 
                html.Div(children=[
                    team_W_L_check(toronto_row),
                    dbc.Col([
                        html.H6(pitch_away)
                        ], width={'size':'auto'}),
                    dbc.Col([
                        html.H6(pitch_home)
                        ], width={'size':'auto'})
                ],style={
                'display': 'inline-flex',
                'justify-content': 'space-between',
                'width': '100%',
                'margin-left': '10px',
                'margin-right':'10px'}
            )
                ]),
            
            ],
                style={
                'margin-left': '0',      
                'margin-right': 'auto',  
                'border': '1px solid black',  
                'padding': '5px',
                'border-radius': '10px',
                'backgroundColor': '#002D62',
                'color': 'white'
                
            }),
        ],
        fluid=True
        ),
        ], width=6),    
        dbc.Col([
            dbc.Container([
                dcc.Interval(id='interval-component', interval=5000, n_intervals=0), 
                html.Div(id='team-display'),
            ], style={
                'color' : '#002D62'})
        ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                html.H2("Gameday summary"),
                game_summary(toronto_row)



])

])
    
               
])


@callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@callback(
    Output('team-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_team_display(n):
    not_toronto_row = df[(df['away_name'] != 'Toronto Blue Jays') & (df['home_name'] != 'Toronto Blue Jays')] 
    team = not_toronto_row.iloc[n % len(not_toronto_row)] 
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                    html.P(team['away_name']),
                ],width={"size":"auto"},
                ),
                dbc.Col([
                    html.P("@"),

                    ], 
                       width={"size":"auto"}, 
                       align='center'),
                dbc.Col([
                    html.P(team['home_name']),

                    ],width={"size":"auto"},)
            ],style={
                'display': 'inline-flex',
                'justify-content': 'space-between',
                'width': '100%',
                'margin-left': '10px',
                'margin-right':'10px'
                }
            ),
        dbc.Row([
                dbc.Col([
                    html.H4(team['away_score']),

                    ], width={"size":"auto"}),
                dbc.Col([
                    html.Div([
                html.H6(f'{team['inning_state']} {team['current_inning']}' ),
                    ]),
                    ],width={'size':'auto'}),
                dbc.Col([
                    html.H4(team['home_score']), 
                     ], width={"size":"auto"},), 
             ],style={
                'display': 'inline-flex',
                'justify-content': 'space-between',
                'width': '100%',
                'margin-left': '10px',
                'margin-right':'10px'
                }
            )
            ],  style={
                'border': '2px solid #002D62',
                'padding': '5px',
                'border-radius': '10px',
                'padding-right':'10px',
                'color': '#002D62'
            })

