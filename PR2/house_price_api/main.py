from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Load the trained model
model_data = joblib.load("model.pkl")
model = model_data['model']
features = model_data['features']

app = FastAPI(title="House Price Prediction API")

class HouseData(BaseModel):
    GrLivArea: float
    YearBuilt: int
    TotalBsmtSF: float
    GarageCars: int

@app.post("/predict")
def predict_price(data: HouseData):
    input_data = [[
        data.GrLivArea,
        data.YearBuilt,
        data.TotalBsmtSF,
        data.GarageCars
    ]]
    prediction = model.predict(input_data)[0]
    return {"predicted_price": round(prediction, 2)}
