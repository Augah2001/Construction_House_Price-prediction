import pickle
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from tensorflow.keras.models import load_model

class Construction(BaseModel):
    building_height: float
    builtup_area: float
    number_of_stories: int
    number_of_rooms: int
    building_function: str
    number_of_units: int

class BMIdata(BaseModel):
    inflationrate: float
    imports: float
    exports: float
    moneysupplym1: float  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=False,  # Set to True if you need to send cookies across origins
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allow all headers sent by the client
)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model1.pkl', 'rb') as f:
    model1 = pickle.load(f)
   
with open('transformer.pkl', 'rb') as f:
    transformer = pickle.load(f)
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.post('/predict')
async def predict(data: Construction):
    point = {
        "number_of_units": data.number_of_units,
        "building_height": data.building_height,
        "builtup_area": data.builtup_area,
        "number_of_stories": data.number_of_stories,
        "number_of_columns": data.number_of_stories,  # assuming number_of_stories is used for columns
        "number_of_rooms": data.number_of_rooms,
        "building_function": data.building_function
    }
    
    df = pd.DataFrame(pd.Series(point)).T
    df_transformed = transformer.transform(df)
    pred = np.expm1(model.predict(df_transformed))
    print(pred)
    return pred.tolist()[0][0]

@app.post('/predictBMI')
async def predict_bmi(dat: BMIdata):
    point = {
        "inflationrate": dat.inflationrate,
        "imports": dat.imports,
        "exports": dat.exports,
        "moneysupplym1": dat.moneysupplym1
    }
    
    df = pd.DataFrame(pd.Series(point)).T
    scaled = scaler.transform(df)
    pred = np.expm1(model1.predict(scaled))
    return (pred.tolist()[0]/100)* 8

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
