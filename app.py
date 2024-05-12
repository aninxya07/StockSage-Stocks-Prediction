import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import datetime as dt

app = dash.Dash(__name__, use_pages=True, prevent_initial_callbacks='initial_duplicate', pages_folder="../pages")

server = app.server

app.layout = html.Div(className='container', children=[
    html.Div(className='navbar', children=[
        html.Span(className='appName', children="S T O C K S A G E"),
        html.Div(className='navlist', children=[
            # html.Li(dcc.Link(className='navlink', children='Home', href='/'), id='tab-home'),
            # html.Li(dcc.Link(className='navlink', children='View', href='/view'), id='tab-view'),
            # html.Li(dcc.Link(className='navlink', children='Indicators', href='/indicators'), id='tab-indicators'),
            dcc.Link(className='navlink', children='Predict', href='/predict'),
        ]),
    ]),
    dash.page_container,
])

    

if __name__ == '__main__':
    app.run_server(debug=True)