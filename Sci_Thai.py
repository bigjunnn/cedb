import pandas as pd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class Sci_Thai:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        # Convert categorical to numerical values
        le = preprocessing.LabelEncoder()
        self.df['Food'] = le.fit_transform(self.df['Food'])
        self.df['Gender'] = le.fit_transform(self.df['Gender'])

        # Setting of the target column and predictors
        target_column = ['Fullness']
        predictors = ['Gender', 'Weight', 'Height', 'BMI Index', 'Food']

        # Create training and data sets
        X = self.df[predictors].values
        y = self.df[target_column].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=10)
        self.lr = LinearRegression()
        self.lr.fit(X_train, y_train)

    def predict(self, curr_values):
        return self.lr.predict(curr_values)

    def add_user_data(self, gender, height, weight, food, fullness):
        curr_bmi = weight/pow(height, 2)
        curr_data = pd.DataFrame({
            "Gender" : [gender],
            "Height" : [height],
            "Weight" : [weight],
            "BMI Index" : [curr_bmi],
            "Food" : [food],
            "Fullness" :[fullness]
        })

        self.df = self.df.append(curr_data)
        print(self.df.tail(3))

    def retrain(self):
        # Convert categorical to numerical values
        le = preprocessing.LabelEncoder()
        self.df['Food'] = le.fit_transform(self.df['Food'])
        self.df['Gender'] = le.fit_transform(self.df['Gender'])

        # Setting of the target column and predictors
        target_column = ['Fullness']
        predictors = ['Gender', 'Weight', 'Height', 'BMI Index', 'Food']

        # Create training and data sets
        X = self.df[predictors].values
        y = self.df[target_column].values

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=10)
        self.lr = LinearRegression()
        self.lr.fit(X_train, y_train)
