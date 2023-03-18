from dash import Dash, html, dcc, Output, Input, dash_table
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import sys, pathlib
import pandas as pd
import os
import numpy as np 
import plotly.express as px

current_folder = pathlib.Path(__file__).parent.resolve()
src_folder = str(current_folder.parent.absolute())
if src_folder not in sys.path:
	sys.path.insert(0, src_folder)

load_figure_template('SIMPLEX')

app = Dash(__name__,external_stylesheets=[dbc.themes.SIMPLEX])

df = pd.read_excel(os.path.join(src_folder, "net_zero_tracker_canada.xlsx"))
canada = df[df["country"]=="CAN"]
corporations = canada[canada["actor_type"]=="Company"]
sector = corporations["industry"].fillna("Other").unique().tolist()
sector.append("All")

d_target = pd.DataFrame({
	"Points": [0, 1, 2],
	"Target": ["No target", "Net zero", "Emission reduction"]
})

d_status = pd.DataFrame({
	"Points": [0, 1, 2, 3],
	"Status": ["No target", "Proposed", "Pledge", "In corporate strategy"]
})

d_plan = pd.DataFrame({
	"Points": [0, 1, 2],
	"Detailed plan": ["Red", "Yellow", "Green"]
})

d_reporting = pd.DataFrame({
	"Points": [0, 1, 2],
	"Reporting Mechanism": ["Red", "Yellow", "Green"]
})

d_scope = pd.DataFrame({
	"Points": [0, 1, 2],
	"Scope 3 Coverage": ["Red", "Yellow", "Green"]
})

d_carbon = pd.DataFrame({
	"Points": [0, 1, 2],
	"Carbon Credits": ["Red", "Yellow", "Green"]
})

app.layout = html.Div([
	html.H1("Holding Canadian companies accountable on climate promises",style={"margin-left": "10px","margin-top":"20px", "margin-bottom":"20px"}),
	html.Div([dcc.Graph(id='climate-graph', figure={}, style={"margin-left":"10px",'width': '80%', 'display': 'inline-block','verticalAlign': 'top'}), html.Img(src='assets/legend.png', height='280', style={'width': '10%', 'display': 'inline-block', 'verticalAlign': 'top'})]),
	html.Div([html.H6("Sector: "), dcc.Dropdown(options=sector, value='All', id='sector')], style={"margin-left":"10px","margin-bottom":"20px",'width': '40%', 'display': 'inline-block'}),
	html.Br(),
	html.H6("Calculation of strength of climate pledge: ",style={"margin-left": "10px","margin-top":"20px"}),
	html.Div([html.Div([dash_table.DataTable(d_target.to_dict('records'), [{"name":i, "id":i} for i in d_target.columns])], style={"margin-left":"10px","margin-right":"10px","margin-bottom":"70px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'}),
			html.Div([dash_table.DataTable(d_status.to_dict('records'), [{"name":i, "id":i} for i in d_status.columns])], style={"margin-left":"20px","margin-bottom":"70px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'}),
			html.Div([dash_table.DataTable(d_plan.to_dict('records'), [{"name":i, "id":i} for i in d_plan.columns])], style={"margin-left":"20px","margin-bottom":"70px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'})
			]),
	html.Div([html.Div([dash_table.DataTable(d_reporting.to_dict('records'), [{"name":i, "id":i} for i in d_reporting.columns])], style={"margin-left":"20px","margin-bottom":"100px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'}),
			html.Div([dash_table.DataTable(d_scope.to_dict('records'), [{"name":i, "id":i} for i in d_scope.columns])], style={"margin-left":"20px","margin-bottom":"100px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'}),
			html.Div([dash_table.DataTable(d_carbon.to_dict('records'), [{"name":i, "id":i} for i in d_carbon.columns])], style={"margin-left":"20px","margin-bottom":"100px",'width': '20%', 'display': 'inline-block','verticalAlign': 'top'})
			])	
	])

def tracker_to_value(dataframe):
	target_dict = {"No target": 0, "Net zero":10, "Climate neutral":10, "Emissions reduction target":5, "Other":0, "Emissions intensity target":5, "Carbon neutral(ity)":10}
	dataframe["target_score"] = dataframe["end_target"].replace(target_dict)
	np.random.seed(42)
	dataframe["PR_score"] = np.random.uniform(size=len(dataframe))
	return dataframe

def year_to_color(years):
	d = {9999:"No target", 2020:"2020", 2025:"2025", 2030:"2030", 2040:"2040", 2050:"2050"}
	return years.fillna(9999).replace(d)

@app.callback(
	Output('climate-graph', 'figure'),
	Input('sector', 'value')
)
def update_graph(sector):
	df = tracker_to_value(corporations)
	if sector != "All":
		display = df[df["industry"]==sector]
	else:
		display = df
	fig = px.scatter(x=display["PR_score"], 
		  			y=display["target_score"], 
					hover_name=display["name"], 
					size=display["annual_revenue"].fillna(1), 
					color = year_to_color(display["end_target_year"]),
					color_discrete_map = {"No target":"black", "2020":"limegreen", "2025":"lightskyblue", "2030":"navajowhite", "2040":"orange", "2050":"red"},
					labels={'x':"Extent of climate claims", 'y':"Calculated strength of climate pledge"})
	
	fig.update_layout(showlegend=False)
	return fig

if __name__ == '__main__':
    app.run_server(debug=True)