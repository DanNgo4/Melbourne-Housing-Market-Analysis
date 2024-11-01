from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model import RFHousePriceModel
from pydantic import BaseModel
import uvicorn
import pandas as pd
<<<<<<< Updated upstream
import os
=======
import json
from pathlib import Path
from pydantic import BaseModel
>>>>>>> Stashed changes


app = FastAPI()
history_file = Path("query_history.json")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
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


class QueryDetails(BaseModel):
    priceRange: str
    houseType: str
    highlighted: list

@app.post("/save-query")
async def save_query(query: QueryDetails):
    try:
        with open("query_history.json", "r+") as file:
            history = json.load(file)
            history.append(query.dict())  # Append new query to the history
            file.seek(0)
            json.dump(history, file, indent=4)
        return {"status": "success"}
    except Exception as e:
        """ raise HTTPException(status_code=500, detail=str(e)) """
    

@app.get("/query-history")
async def get_query_history():
    try:
        if history_file.exists():
            with open(history_file, "r") as f:
                return json.load(f)
        return []
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)