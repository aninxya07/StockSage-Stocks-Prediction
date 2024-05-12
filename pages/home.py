import dash
from dash import html, dcc
from dash.dependencies import Input, Output

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.Div(className='home-container', children=[
        html.Div(className='home-desc', children=[
            html.Div(className='home-div-left', children=[
                html.Div(className='home-head', children=[
                    html.H1(className='home-h1',children='About StockSage'),
                ]),
                html.Div(className='home-body', children=[
                    html.P(className='home-content', children="Welcome to StockSage! Our app utilizes advanced machine learning to provide accurate stock predictions. Analyzing historical data, market trends, and news, StockSage equips you with actionable insights. Whether you're an experienced investor or just starting out, StockSage helps you make informed decisions in the dynamic stock market. Unlock your investment potential with StockSage today!")
                ]),
                html.Div(className='home-btn-holder', children=[
                    # html.Button('View Stocks', className='home-btn', id='home-view-btn'),
                    # html.Button('View Indicators', className='home-btn', id='home-indicator-btn'),
                    # html.Button('Predict Stock', className='home-btn', id='home-predict-btn')
                    dcc.Link('View Stocks', href='/view', className='home-btn', id='home-view-btn'),
                    dcc.Link('View EMA', href='/ema', className='home-btn', id='home-indicator-btn'),
                    dcc.Link('Predict Stock', href='/predict', className='home-btn', id='home-predict-btn')

                ]),
                html.P('*EMA - Exponential Moving Average', className='home-info'),
                html.P('Disclaimer: This model just provides a general prediction of closing prices in future. However in real life, stock prices depend on several critical factors which are out of the scope of this model to cover. Please invest at your own risk', className='home-info', id='risk-fac')
            ]),
            html.Div(className='home-div-right', children=[
                html.Img(src='./assets/undraw_investing_re_bov7.svg', className='home-mainImg'),
            ]),
        ])
    ])
], className='home')
