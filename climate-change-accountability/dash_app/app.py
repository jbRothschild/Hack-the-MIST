from dash import Dash, html, dcc, Output, Input
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import sys, pathlib
import pandas as pd
import os
import numpy as np 

current_folder = pathlib.Path(__file__).parent.resolve()
src_folder = str(current_folder.parent.absolute())
if src_folder not in sys.path:
	sys.path.insert(0, src_folder)

load_figure_template('SIMPLEX')

app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.SIMPLEX])

df = pd.read_excel(os.path.join(src_folder, "net_zero_tracker_canada.xlsx"))
canada = df[df["country"]=="CAN"]
corporations = canada[canada["actor_type"]=="Company"]
PR = np.random.uniform(len(corporations))

app.layout = html.Div([
	html.H1("Holding Canadian companies accountable for their climate pledges"),
	dcc.Graph(id='climate-graph'),
	html.Div["Sector: ", dcc.Dropdown(canada["industry"].unique.tolist().append('All'), 'All', id='sector')]
])

@app.callback(
	Output('climate-graph', 'figure'),
	Input('sector', 'value')
)
def update_graph()