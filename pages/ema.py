import dash
from dash import dcc, html, Input, Output, State, callback
from datetime import date
from dateutil.relativedelta import relativedelta

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


dash.register_page(__name__)



layout = html.Div(className='view-container', children=[
    html.Div(className='inputs', children=[
        html.Div(className='view-header', children=[
            html.H2('View EMA')
        ]),
        html.Div(className='stockNameInput', children=[
            html.Div(className='inputBox', children=[
                dcc.Input(id='ema-stock-code-inp', required='required', autoComplete='off'),
                html.Span('Input Stock Code'),
            ]),
            html.Button('See Company Details', id='ema-comp-details')
        ]),
        html.Div(className='view-btn', children=[
            html.Button('View EMA', className='view-stk-btn', id='ema-stk-btn')
        ]),
        html.Div(className='ema-btn-holder', children=[
            dcc.Link(className='back-home', children='Home', href='/'),
            dcc.Link(className='back-view', children='View Stocks', href='/view'),
        ])
    ]),
    html.Div([
        html.Div(children=[  
            # Company Name
            html.Div(children=[

            ], id='ema-comp-name'),
            # Company Website
            html.Div(children=[
                
            ], id='ema-comp-web')
        ], className="header", id='ema-header'),

        # Company Description
        html.Div(children=[

        ], id="ema-description", className="decription_ticker"),
        html.Div([
            # Stock price plot
        ], id="ema-ohlc-graphs-content"),
        html.Div([
            # Indicator plot
        ], id="main-content"),
        html.Div([
            # Forecast plot
        ], id="forecast-content")
    ], className="content"),
])

@callback(
    Output('ema-comp-name', 'children', allow_duplicate=True),
    [Input('ema-comp-details', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')],
    prevent_initial_call = True
)
def displayCompanyName(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            df = pd.DataFrame().from_dict(info, orient='index').T

            return f"{df['longName'][0]}"
        except:
            return f"Please enter valid Stock Code"
    else:
        return ""
    
@callback(
    Output('ema-description', 'children', allow_duplicate=True),
    [Input('ema-comp-details', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')],
    prevent_initial_call = True
)
def displayCompanyInfo(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info


            return f"{info['longBusinessSummary']}"
        except:
            return ""
    else:
        return ""
    
@callback(
    Output('ema-comp-web', 'children', allow_duplicate=True),
    [Input('ema-comp-details', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')],
    prevent_initial_call = True
)
def displayCompanyWebsite(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            df = pd.DataFrame().from_dict(info, orient='index').T

            return f"Website: {info['website']}"
        except:
            return f"Please enter valid Stock Code"
    else:
        return ""

@callback(
    Output('ema-ohlc-graphs-content', 'children', allow_duplicate=True),
    [Input('ema-comp-details', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')],
    prevent_initial_call = True
)
def displayCompanyWebsite(n_clicks, stock_code):
    return ""
    
def getEMAGraph(df, compName):
    df['EWA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
    # fig = go.Figure(go.Ohlc(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
    fig = px.scatter(df, x=df['Date'], y=df['EWA_20'])
    fig.update_layout(template='plotly_dark', title=f'{compName} Exponential Moving Average vs Date (in USD)')
    
    return fig

@callback(
    Output('ema-comp-name', 'children'),
    [Input('ema-stk-btn', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')]
)
def displayCompanyName(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            df = pd.DataFrame().from_dict(info, orient='index').T

            return f"{df['longName'][0]}"
        except:
            return f""
    else:
        return ""
    
@callback(
    Output('ema-description', 'children'),
    [Input('ema-stk-btn', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')]
)
def displayCompanyInfo(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info

            return f"{info['longBusinessSummary']}"
        except:
            return ""
    else:
        return ""
    
@callback(
    Output('ema-comp-web', 'children'),
    [Input('ema-stk-btn', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')]
)
def displayCompanyWebsite(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            df = pd.DataFrame().from_dict(info, orient='index').T

            return f"Website: {info['website']}"
        except:
            return f"Please enter valid Stock Code"
    else:
        return ""
    
@callback(
    Output('ema-ohlc-graphs-content', 'children'),
    [Input('ema-stk-btn', 'n_clicks')],
    [State('ema-stock-code-inp', 'value')]
)

def displayStockGraph(n_clicks, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:
            ticker = yf.Ticker(stock_code)
            info = ticker.info
            yearago = str(date.today() - relativedelta(years=1))
            df = yf.download(stock_code, start=yearago, end=str(date.today()))
            df.reset_index(inplace=True)
            for i in ['Open', 'High', 'Close', 'Low']:
                df[i] = df[i].astype('float64')

            fig = getEMAGraph(df, info['shortName'])

            return dcc.Graph(figure = fig)
        except:
            return f""
    else:
        return ""



