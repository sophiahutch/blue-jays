import dash
from dash import dcc, html
import plotly.express as px

dash.register_page(__name__)

df = px.data.tips()

layout = html.Div(
    html.Div("position")
)