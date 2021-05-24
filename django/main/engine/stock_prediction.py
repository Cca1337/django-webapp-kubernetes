import numpy as np
import pandas as pd
import pandas_datareader as web
import datetime as dt
from datetime import date
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from os import path
from os import sep
from os import pardir

# days = 10
# company = 'FB'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cesta = '/usr/src/app'

filepath = f"{cesta}/static/CSV/"
filepath1 = f"{cesta}/static/Pickles/"
filepath2 = f"{cesta}/static/graphs"


def stock_price_prediction(days, company):

    company = company

    today = str(date.today()).split("-")
    year = int(today[0])
    month = int(today[1])
    day = int(today[2])

    start = dt.datetime(2020,1,1)
    end = dt.datetime(year,month,day)

    def get_data():
        # Looks for data
        data = web.DataReader(company, 'yahoo', start, end)
        # Save data to csv
        data.to_csv(f"{filepath}{company}_{days}_prediction.csv")

    if path.exists(f"{filepath}{company}_{days}_prediction.csv"):
        pass
    else:
        get_data()

    # Read data from saved csv file
    data = pd.read_csv(f"{filepath}{company}_{days}_prediction.csv", index_col=0, parse_dates=True)

   # Last ADJ Close value ..To print on screen at the end
    last_value = round(data['Adj Close'][-1], 2)

    # Modified data to have Date as column
    data = data.reset_index()

    # # New collumn HIGH-LOW percentage
    data['HL_pct'] = (data['High']-data['Low'])/data['Low']*100
    # Get only This collumns
    data = data[['Adj Close', 'Volume', 'HL_pct']]

    # # creates new Prediction Column named FUTURE3DAYS which get values from Adj Close and is shifted by prediction time
    predict_col = 'Adj Close'
    # # Fills all N/a values with zeros
    data.fillna(0, inplace=True)

    # # Number of days we want to predict
    prediction_days = days

    data['Future3days'] = data[predict_col].shift(-prediction_days)

    # Drops rows which have NaN
    data.dropna(inplace=True)

    # # input variables to train model ...1 means drop collumns zero would drop rows
    X = np.array(data.drop(['Future3days'], 1))
    X = preprocessing.scale(X)
    y = np.array(data['Future3days'])

    # # 70percent train data and 30 percent of test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    # # Multiple Linear Regression model
    # #classifier definition
    clf = LinearRegression()
    clf.fit(X_train, y_train)

    # # Load clasifier from pickle file
    if path.exists(f"{filepath1}{company}_{days}_predictionmodel.pickle"):
        with open(f"{filepath1}{company}_{days}_predictionmodel.pickle", 'rb') as f:
            clf = pickle.load(f)
            # # Load clasifier from pickle file

    else:
        # # save clasifier to pickle format that way we dont have to train our model all the time just once
        with open(f"{filepath1}{company}_{days}_predictionmodel.pickle", 'wb') as f:
            pickle.dump(clf, f)

    # # confidence aka accuracy
    confidence = clf.score(X_train, y_train)
#   print("Accuracy >>> ", confidence)

# WE CAN TEST OUR MODEL
    #for X,y in zip(X_test, y_test):
#       print(f"Model predicted price (3days in future): {clf.predict([X])[0]}, Actual price at 3 days later: {y}")

    #----------------------------------------------------------------------#
    data_test = pd.read_csv(f"{filepath}{company}_{days}_prediction.csv", index_col=0)
    # # Modified data to have Date as column
    data_test_modified = data_test.reset_index()

    # New collumn
    data_test['HL_pct'] = (data_test['High']-data_test['Low'])/data_test['Low']*100

    # # Get only This collumns
    data_test = data_test[['Adj Close', 'Volume', 'HL_pct']]

    X_new = np.array(data_test)
    X_new = preprocessing.scale(X_new)

    a = []
    for x in (X_new):
        #print(f"Model predicted price: that is going to be 3 days later: {clf.predict([x])[0]} ")
        a.append(clf.predict([x])[0])

    column = 'Predictions'
    data_test_modified[column] = a

    ibaPredictions = data_test_modified['Predictions']
    vysledok = data_test_modified['Predictions'].tail(1)
    #vyber je do graphu doplnit predikovane hodnoty na prediction days
    vyber = data_test_modified['Predictions'][-prediction_days:]

    for x in range(prediction_days):
        ibaPredictions.loc[len(ibaPredictions)] = 0

    ibaPredictions = ibaPredictions.shift(prediction_days)

    x_axis = data_test_modified['Date']
    y_axis = data_test_modified['Adj Close']

    posledna = str(data_test_modified['Adj Close'].tail(1))
    riadok = int(posledna.split(" ")[0])

    hodnota = posledna.split('\n')[0]
    hodnota = float(hodnota.split(" ")[4])


    ibaPredictions.loc[riadok] = hodnota

    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(20))

    plt.plot(x_axis, y_axis, color='blue', linewidth=0.5, label='Actual price')
    plt.plot(ibaPredictions.tail(prediction_days+1), color='red', linewidth=1, label='Prediction')

    plt.title(f'Stock Market {company}')
    plt.xlabel('Dates')
    plt.xticks(rotation=45)
    plt.ylabel('Price')

    #plt.grid(True)
    plt.legend()


    ulozenka = plt.savefig(f"{filepath2}/{company}_{days}_prediction.png", bbox_inches="tight")

    plt.clf()
    plt.cla()
    plt.close(ulozenka)

    prediction = round(ibaPredictions.values[-1], 3)

    return prediction, last_value, filepath2


#stock_price_prediction(days, company)
