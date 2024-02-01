from dash import Dash, html, dcc, Output, Input, dash_table, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
countries = df['country'].unique()

app = Dash(
    external_stylesheets=[dbc.themes.VAPOR]
)

app.layout = html.Div([
    dbc.Container([
    dbc.Row(
    html.H1(children='Welcome to Dash Workshop!'),  align="center"),
    ]),
    html.Br(),
    dcc.Dropdown(options=['boxplot', 'histogram'], value='histogram', id='drop_down_graph', className='drop_style'),
    dcc.Dropdown(options=countries, id='drop_down_country', className='drop_style'),
    dcc.Graph(id='graph'),
    html.Br(),
    dbc.Container([
    dbc.Row(children=[
    dbc.Col(dcc.Dropdown(options=df.select_dtypes(include=np.number).columns, value=df.columns[1], id='drop_down_cols', className='drop_style'),),
    dbc.Col(dcc.Dropdown(options=['>', '<', '='], value='>', id='drop_down_sign', className='drop_style'),),
    dbc.Col(dcc.Dropdown(id='drop_down_filter', className='drop_style'),),
    dbc.Col(html.Button('Submit', id='submit-val', n_clicks=0),)
    ])
    ]),
    dash_table.DataTable(
        id='table',
        data=df.to_dict('records'),
       ),

])

@app.callback(
    Output("graph", 'figure'),
    Input("drop_down_graph", 'value'),
    Input("drop_down_country", 'value'),
)

def show_plot(dd_graph_val, dd_country_val):
    filtered_data = df.query(f'country == "{dd_country_val}"')
    if dd_graph_val == 'boxplot':
        fig = px.box(filtered_data, x='lifeExp')
    if dd_graph_val == 'histogram':
        fig = px.histogram(filtered_data, x='lifeExp')
    return fig


@app.callback(
    Output('drop_down_filter', 'options'),
    Input('drop_down_cols', 'value'),
)
def show_table(selected_col):
    dd_unique_vals = df[selected_col].unique()
    dd_options = [{"label": r, "value": r} for r in dd_unique_vals]
    return dd_options


@app.callback(
    Output("table", 'data'),
    Input('drop_down_cols', 'value'),
    Input('drop_down_sign', 'value'),
    Input('drop_down_filter', 'value'),
    Input('submit-val', 'n_clicks'),

)
def press(dd_cols, dd_sign, num_filter, click):
    changed = [p['prop_id'] for p in callback_context.triggered][0]
    if 'submit-val' in changed:
        data = df.query(f'{dd_cols} {dd_sign} {num_filter}')
        return data.to_dict('records')


if __name__ == '__main__':
    app.run(debug=False, port=8051, host="0.0.0.0")