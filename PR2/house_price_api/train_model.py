import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

class HousePricePredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.features = ['GrLivArea', 'YearBuilt', 'TotalBsmtSF', 'GarageCars']
    
    def load_and_preprocess_data(self, path="train.csv"):
        df = pd.read_csv(path)
        df = df[self.features + ['SalePrice']].dropna()
        X = df[self.features]
        y = df['SalePrice']
        return X, y

    def train(self, X, y):
        self.model.fit(X, y)

    def save_model(self, path="model.pkl"):
        joblib.dump({'model': self.model, 'features': self.features}, path)

if __name__ == "__main__":
    predictor = HousePricePredictor()
    X, y = predictor.load_and_preprocess_data()
    predictor.train(X, y)
    predictor.save_model()
