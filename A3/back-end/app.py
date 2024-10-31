from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from model import RFHousePriceModel
import pandas as pd


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = RFHousePriceModel()


@app.get("/")
async def root():
    return {"message": "Welcome to the House Price Prediction API"}


@app.get("/predicted_values/")
async def predicted_values():
    csv_data = pd.read_csv('predicted_values.csv')

    # Convert CSV data to JSON
    json_data = csv_data.to_dict(orient='records')

    return JSONResponse(content=json_data, media_type="application/json")


@app.get("/predict/{square_metres}/{distance}/{propertycount}/")
async def predict_price(square_metres: float, distance: float, propertycount: int):
    print(f"Received request with square_metres={square_metres}, distance={distance}, propertycount={propertycount}")
    price = model.predict(square_metres, distance, propertycount)[0]
    return {"predicted_price": price}



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

    print(model.predict(440, 12, 4000))
