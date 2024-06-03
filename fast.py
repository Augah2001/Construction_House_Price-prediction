import pickle 
from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class Construction(BaseModel):
    building_height: float
    builtup_area: float # type: ignore
    number_of_stories: int# type: ignore
    number_of_columns: int # type: ignore
    number_of_rooms : int # type: ignore
    building_function: str # type: ignore
    number_of_units: int # type: ignore
    


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
   
with open('transformer.pkl', 'rb') as f:
    transformer = pickle.load(f)


@app.post('/predict')
async def predict(data: Construction):
    point = {"number_of_units" : data.number_of_units,
                       "building_height": data.building_height,
                      "builtup_area": data.builtup_area,
                      "number_of_stories": data.number_of_stories,
                      "number_of_columns": data.number_of_stories,
                      "number_of_rooms": data.number_of_rooms,
                      "building_function": data.building_function}
    
    df =pd.DataFrame( pd.Series(point)).T
    df_transformed =  transformer.transform(df)
    pred = model.predict(df_transformed)
    print(pred)
    return pred.tolist()[0][0]