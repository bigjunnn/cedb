import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class SCI_THAI:
    def __init__(self, data_path):
        df = pd.read_csv(data_path)
        # Convert categorical to numerical values
        le = preprocessing.LabelEncoder()
        df['Food'] = le.fit_transform(df['Food'])
        df['Gender'] = le.fit_transform(df['Gender'])

        # Setting of the target column and predictors
        target_column = ['Fullness']
        predictors = list(set(list(df.columns))-set(target_column))

        # Create training and data sets
        X = df[predictors].values
        y = df[target_column].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=10)
        self.lr = LinearRegression()
        self.lr.fit(X_train, y_train)

    def predict(self, curr_values):
        return self.lr.predict(curr_values)

    def retrain(self, datapath):
        df = pd.read_csv(data_path)
        # Convert categorical to numerical values
        le = preprocessing.LabelEncoder()
        df['Gender'] = le.fit_transform(df['Gender'])
        df['Food'] = le.fit_transform(df['Food'])

        # Setting of the target column and predictors
        target_column = ['Fullness']
        predictors = list(set(list(df.columns))-set(target_column))

        # Create training and data sets
        X = df[predictors].values
        y = df[target_column].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=10)

        self.lr = LinearRegression()
        self.lr.fit(X_train, y_train)
