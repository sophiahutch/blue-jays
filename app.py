import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.UNITED, dbc.icons.BOOTSTRAP],suppress_callback_exceptions=True, use_pages=True)

app.layout = html.Div(
    [


            dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col([
                        html.Img(src="assets/jayspic.jpg", height='60px'),
                        dbc.NavbarBrand('Toronto Blue Jays App', className='ms-2'),
                    ],
                    width={"size":"auto"}),
                    ],
                    align="center",
                    className="g-0"
                ), 
            
            
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Collapse(
                        dbc.Nav([
                            html.Div([
                                dcc.Link(page['name'] + " | ", href=page['path'], style={'color': 'white'})
                                for page in dash.page_registry.values()
                            ]),
                            ]),
                        id="navbar-collapse",
                        is_open=False,
                        navbar=True,
                    )
                    ], width={"size":"auto"},
                    ),
                ],
                align="center",
            ),
            dbc.Col(dbc.NavbarToggler(id="navbar-toggler", n_clicks=0)),

            dbc.Row(
                [
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink(html.I(className='bi bi-github'), href="https://github.com/sophiahutch/blue-jays", external_link=True)),
                            dbc.NavItem(dbc.NavLink(html.I(className='bi bi-linkedin'), href="https://www.linkedin.com/in/sophia-hutchison/", external_link=True)),
                    ])
                    ], width={"size":"auto"}),
                ],
                align="center"
                
            ),
               
        ],
        fluid= True
    ),
    color = '#002D62',
    dark=True
    ),
        dash.page_container
    ]
)


if __name__ == "__main__":
    app.run(debug=True)
