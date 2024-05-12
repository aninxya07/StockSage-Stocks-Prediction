import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np

def getStockData(stock_code):
    ticker = yf.Ticker(stock_code)
    data = ticker.history(period='365d')
    pd.set_option('display.max_columns', None)
    pd.set_option('display.float_format', lambda x: '%.5f' % x)
    df = pd.DataFrame.from_dict(data)
    df = df.dropna()
    df = df.drop(columns=['Volume', 'Dividends', 'Stock Splits', 'Open', 'High', 'Low'])
    return df

def predictStockPrice(df, days):
    forecast_days = days

    df['Predictions'] = df['Close'].shift(-forecast_days)

    X = np.array(df.drop(columns=['Predictions'], axis=1))
    data = [X[-1, :]]

    X = X[:-forecast_days]

    y = np.array(df['Predictions'])

    y = y[:-forecast_days]

    X_train, x_test, Y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=4)

    regr = LinearRegression().fit(X_train, Y_train)

    yhat = regr.predict(x_test)

    predData = data
    predList = []
    for i in range(forecast_days):
        predList.append(regr.predict(predData))
        predData = [predList[-1]]

    predictions = []

    for i in predList:
        predictions.append(i[0])
    

    return predictions

   




