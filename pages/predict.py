import dash
from dash import dcc, html, Input, Output, State, callback
from datetime import date
from dateutil.relativedelta import relativedelta

import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import model, sys, os


dash.register_page(__name__)



layout = html.Div(className='view-container', children=[
    html.Div(className='inputs', children=[
        html.Div(className='view-header', children=[
            html.H2('Predict Stock')
        ]),
        html.Div(className='stockNameInput', children=[
            html.Div(className='inputBox', children=[
                dcc.Input(id='pred-stock-code-inp', required='required', autoComplete='off'),
                html.Span('Input Stock Code'),
            ]),
            html.Div(className='inputBox', children=[
                dcc.Input(id='pred-days-inp', required='required', autoComplete='off'),
                html.Span('Input No. of days'),
            ]),
            html.Button('See Company Details', id='pred-comp-details')
        ]),
        html.Div(className='view-btn', children=[
            html.Button('Predict Stock', className='view-stk-btn', id='pred-stk-btn')
        ]),
        html.Div(className='pred-btn-holder', children=[
            dcc.Link(className='back-home', children='Home', href='/'),
            dcc.Link(className='back-view', children='View Stocks', href='/view'),
            dcc.Link(className='back-ema', children='EMA', href='/ema')
        ])
        

    ]),
    html.Div([
        html.Div(children=[  
            # Company Name
            html.Div(children=[

            ], id='pred-comp-name'),
            # Company Website
            html.Div(children=[
                
            ], id='pred-comp-web')
        ], className="header", id='pred-header'),

        # Company Description
        html.Div(children=[

        ], id="pred-description", className="decription_ticker"),
        html.Div([
            # Stock price plot
        ], id="pred-ohlc-graphs-content"),
        html.Div([
            # Indicator plot
        ], id="main-content"),
        html.Div([
            # Forecast plot
        ], id="forecast-content")
    ], className="content"),
])

@callback(
    Output('pred-comp-name', 'children', allow_duplicate=True),
    [Input('pred-comp-details', 'n_clicks')],
    [State('pred-stock-code-inp', 'value')],
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
    Output('pred-description', 'children', allow_duplicate=True),
    [Input('pred-comp-details', 'n_clicks')],
    [State('pred-stock-code-inp', 'value')],
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
    Output('pred-comp-web', 'children', allow_duplicate=True),
    [Input('pred-comp-details', 'n_clicks')],
    [State('pred-stock-code-inp', 'value')],
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
    Output('pred-ohlc-graphs-content', 'children', allow_duplicate=True),
    [Input('pred-stk-btn', 'n_clicks')],
    [State('pred-days-inp', 'value')],
    prevent_initial_call = True
)
def displayCompanyWebsite(n_clicks, stock_code):
    return ""
    
def getpredGraph(compName, days, predictions):
    dateList = []
    for i in range(days):
        dateList.append(str((date.today() + relativedelta(days=i+1)).strftime('%d-%m-%Y')))

    dataFrame = pd.DataFrame(dict(x = dateList, y = predictions))

    dataFrame = dataFrame.rename(columns={'x':'Date', 'y':'Closing Price Prediction'})

    fig = px.line(dataFrame, x='Date', y='Closing Price Prediction', markers=True)
    fig.update_layout(template='plotly_dark', title=f'{compName} Closing Price Prediction vs Date (in USD)')
    
    return fig

@callback(
    Output('pred-comp-name', 'children'),
    [Input('pred-stk-btn', 'n_clicks')],
    [State('pred-days-inp', 'value'), State('pred-stock-code-inp', 'value')]
)
def displayCompanyName(n_clicks, days, stock_code):
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
    Output('pred-description', 'children'),
    [Input('pred-stk-btn', 'n_clicks')],
    [State('pred-days-inp', 'value'), State('pred-stock-code-inp', 'value')]
)
def displayCompanyInfo(n_clicks, days, stock_code):
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
    Output('pred-comp-web', 'children'),
    [Input('pred-stk-btn', 'n_clicks')],
    [State('pred-days-inp', 'value'), State('pred-stock-code-inp', 'value')]
)
def displayCompanyWebsite(n_clicks, days, stock_code):
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
    Output('pred-ohlc-graphs-content', 'children'),
    [Input('pred-stk-btn', 'n_clicks')],
    [State('pred-days-inp', 'value'), State('pred-stock-code-inp', 'value')]
)

def displayStockGraph(n_clicks, days, stock_code):
    if n_clicks is None:
        return ""
    elif stock_code:
        try:

            ticker = yf.Ticker(stock_code)
            info = ticker.info
    
            frame = model.getStockData(stock_code)

            predictions = model.predictStockPrice(frame, int(days))

            fig = getpredGraph(info['longName'], days=int(days), predictions=predictions)

            return dcc.Graph(figure = fig)
        except Exception as error:
            return f"Some unexpected error occurred. Possible reasons: 1. Connection issues  2. Incorrect stock code"
    else:
        return ""



