from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model import RFHousePriceModel
from pydantic import BaseModel
import pandas as pd
import os


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = RFHousePriceModel()

class NewPredictedValues(BaseModel):
    Landsize: float
    Distance: float
    Room: int
    Car: int

@app.get("/predicted_values/")
async def predicted_values():
    csv_data = pd.read_csv('predicted_values.csv')

    # Convert CSV data to JSON
    json_data = csv_data.to_dict(orient='records')

    return JSONResponse(content=json_data, media_type="application/json")


@app.get("/predict/{square_metres}/{distance}/{rooms}/{cars}")
async def predict_price(square_metres: float, distance: float, rooms: int, cars: int):
    print(f"Received request with square_metres={square_metres}, distance={distance}, rooms={rooms}, cars={cars}")
    price = model.predict(square_metres, distance, rooms, cars)[0]
    return {"predicted_price": price}


@app.post("/add-predicted-values/")
async def add_row(new_values: NewPredictedValues):
    file_path = "predicted_values.csv"

    #Creates CSV files if it doesn't exist
    if not os.path.exists(file_path):
        pd.DataFrame(columns=["Landsize", "Distance", "Room", "Car"]).to_csv(file_path, index=False)

    df = pd.read_csv(file_path)

    new_data = {
        "Landsize": new_values.Landsize,
        "Distance": new_values.Distance,
        "Room": new_values.Room,
        "Car": new_values.Car
    }

    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

    df.to_csv(file_path, index=False)

    return {"message": "values added successfully"}

@app.get("/donut-data")
async def get_donut_data():
    df = pd.read_csv("Melbourne_housing_FULL.csv")

    columns = ["Type", "Price"]

    df = df[columns]

    df = df.dropna(axis=0).reset_index(drop=True)

    data = df.to_json(orient="records")

    return JSONResponse(content=data, media_type="application/json")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)