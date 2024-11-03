from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from regression_model import RFHousePriceModel
from classify_model import RFHouseTypeModel
from pydantic import BaseModel, Field
import uvicorn
import os
import pandas as pd
from utils import logger
from base_models import NewPredictedValues


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Regression Model
model = RFHousePriceModel()
# Classification Model
model_classify = RFHouseTypeModel()

class NewPredictedValues(BaseModel):
    Landsize: float
    Distance: float
    Room: int
    Car: int

@app.get("/predicted_values/")
async def predicted_values():
    try:
        csv_data = pd.read_csv('predicted_values.csv')

        # Convert CSV data to JSON
        json_data = csv_data.to_dict(orient='records')
        
        logger.info(f"Returning: {len(json_data)} predicted values")

        return JSONResponse(content=json_data, media_type="application/json")
    except Exception as e:
            logger.error(f"Error retrieving predicted values: {str(e)}")
            
            raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/predict_price/{square_metres}/{distance}/{rooms}/{cars}")
async def predict_price(
    square_metres: float,
    distance: float,
    rooms: int,
    cars: int
):
    if square_metres <= 0:
        raise HTTPException(status_code=400, detail="Square meters must be greater than 0")
    if distance < 0:
        raise HTTPException(status_code=400, detail="Distance must be non-negative")
    if not (1 <= rooms <= 100):
        raise HTTPException(status_code=400, detail="Rooms must be between 1 and 10")
    if not (0 <= cars <= 50):
        raise HTTPException(status_code=400, detail="Car spaces must be between 0 and 5")
    
    try:
        logger.info(f"Received request with square_metres={square_metres}, distance={distance}, rooms={rooms}, cars={cars}")
        
        price = model.predict(square_metres, distance, rooms, cars)[0]
        logger.info(f'Predicted price: {price}')

        return {"predicted_price": price}
    except Exception as e:
        logger.error(f"Error predicting price: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/add-predicted-values/")
async def add_row(new_values: NewPredictedValues):
    try:
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
        logger.info("Saved new values to CSV!")

        return {"message": "values added successfully"} 
    except Exception as e:
            logger.error(f"Error saving values!: {str(e)}")
            
            raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/donut-data")
async def get_donut_data():
    df = pd.read_csv("Melbourne_housing_FULL.csv")
    df = df[["Type", "Price"]].dropna().reset_index(drop=True)
    data = df.to_json(orient="records")

    return JSONResponse(content=data, media_type="application/json")


@app.get("/predict_type/{square_metres}/{distance}/{rooms}/{cars}")
async def predict_house_type(
    square_metres: float,
    distance: float,
    rooms: int,
    cars: int
):
    if square_metres <= 0:
        raise HTTPException(status_code=400, detail="Square meters must be greater than 0")
    if distance < 0:
        raise HTTPException(status_code=400, detail="Distance must be non-negative")
    if not (1 <= rooms <= 10):
        raise HTTPException(status_code=400, detail="Rooms must be between 1 and 10")
    if not (0 <= cars <= 5):
        raise HTTPException(status_code=400, detail="Car spaces must be between 0 and 5")
    
    try:
        predicted_type = model_classify.classify(square_metres, distance, rooms, cars)
        return {"predicted_type": predicted_type}
    except Exception as e:
        logger.error(f"Error classifying house type: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
