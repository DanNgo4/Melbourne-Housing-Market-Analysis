from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from regression_model import RFHousePriceModel
from classify_model import RFHouseTypeModel
import uvicorn
import os
import pandas as pd
from utils import logger
from base_models import NewPredictedValues
import json

app = FastAPI()

#Added CORS middle ware to allow cross orgins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Regression Model
model_regress = RFHousePriceModel()
# Classification Model
model_classify = RFHouseTypeModel()


# This a a GET route that retrieves all the values from
# predicted_values.csv to serve the frontend in the line chart
@app.get("/predicted_values/")
async def predicted_values():
    try:
        csv_data = pd.read_csv("./datasets/predicted_values.csv")

        # Convert CSV data to JSON
        json_data = csv_data.to_dict(orient='records')
        
        logger.info(f"Returning: {len(json_data)} predicted values")

        return JSONResponse(content=json_data, media_type="application/json")
    except Exception as e:
            logger.error(f"Error retrieving predicted values: {str(e)}")
            
            raise HTTPException(status_code=500, detail="Internal server error")


# This is a GET Route where with 4 inputs the model can be queried to return the price prediction
@app.get("/predict_price/{square_metres}/{distance}/{rooms}/{cars}")
async def predict_price(
    square_metres: float,
    distance: float,
    rooms: int,
    cars: int
):
      # Input Validation
    if square_metres <= 0:
        raise HTTPException(status_code=422, detail="Square meters must be greater than 0")
    if distance < 0:
        raise HTTPException(status_code=422, detail="Distance must be non-negative")
    if not (1 <= rooms <= 100):
        raise HTTPException(status_code=422, detail="Rooms must be between 1 and 10")
    if not (0 <= cars <= 50):
        raise HTTPException(status_code=422, detail="Car spaces must be between 0 and 5")
    
    try:
        logger.info(f"Received request with square_metres={square_metres}, distance={distance}, rooms={rooms}, cars={cars}")
        
        # Calling model to predict price
        price = model_regress.predict(square_metres, distance, rooms, cars)[0]
        logger.info(f'Predicted price: {price}')

        return {"predicted_price": price}
    except Exception as e:
        logger.error(f"Error predicting price: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


# This is a POST route so values can be saved to the CSV file
@app.post("/add-predicted-values/")
async def save_to_csv(new_values: NewPredictedValues):
    try:
        file_path = "predicted_values.csv"

        # Creates CSV files if it doesn't exist
        if not os.path.exists(file_path):
            pd.DataFrame(columns=["Landsize", "Distance", "Room", "Car"]).to_csv(file_path, index=False)

        df = pd.read_csv(file_path)

        # Create the JSON object to send into the Dataframe which is modelling the CSV
        new_data = {
            "Landsize": new_values.Landsize,
            "Distance": new_values.Distance,
            "Room": new_values.Room,
            "Car": new_values.Car
        }

        # Add the new row to the dataframe
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

        # Set the CSV to the new Dataframe
        df.to_csv(file_path, index=False)
        logger.info("Saved new values to CSV!")

        return {"message": "values added successfully"} 
    except Exception as e:
            logger.error(f"Error saving values!: {str(e)}")
            
            raise HTTPException(status_code=500, detail="Internal server error")


# This is a GET route so Donut component can get all the records from the melbourne housing dataset
# where only "type" and "price" attributes are kept
@app.get("/donut-data")
async def get_donut_data():
    df = pd.read_csv("./datasets/Melbourne_housing_FULL.csv")
    df = df[["Type", "Price"]].dropna().reset_index(drop=True)
    data = df.to_json(orient="records")

    return JSONResponse(content=data, media_type="application/json")


# This is a GET route that predicts the type of a house based on the passed in parameters
@app.get("/predict_type/{square_metres}/{distance}/{rooms}/{cars}")
async def predict_house_type(
    square_metres: float,
    distance: float,
    rooms: int,
    cars: int
):
    # Input validation
    if square_metres <= 0:
        raise HTTPException(status_code=422, detail="Square meters must be greater than 0")
    if distance < 0:
        raise HTTPException(status_code=422, detail="Distance must be non-negative")
    if not (1 <= rooms <= 10):
        raise HTTPException(status_code=422, detail="Rooms must be between 1 and 10")
    if not (0 <= cars <= 5):
        raise HTTPException(status_code=422, detail="Car spaces must be between 0 and 5")
    
    try:
        # Using classificaiton to predict the house type
        predicted_type = model_classify.classify(square_metres, distance, rooms, cars)
        return {"predicted_type": predicted_type}
    except Exception as e:
        logger.error(f"Error classifying house type: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# This is a GET route tho retrieve GeoJSON data for house prices.
@app.get("/geojson")
async def get_geojson():
    try:
        with open('map.geojson', 'r') as f:
            geojson_data = json.load(f)
        return JSONResponse(content=geojson_data)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="GeoJSON file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing GeoJSON file")


if __name__ == "__main__":
    # Uvircorn will run the API on http://localhost:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
