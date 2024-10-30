from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import RFHousePriceModel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


model = RFHousePriceModel()

@app.get("/")
async def root():
    return {"message": "Welcome to the House Price Prediction API"}

@app.get("/predict/{square_metres}/{car}/{distance}/{propertycount}/")
async def predict_price(square_metres: float, car: bool, distance: float, propertycount: int):
    price = model.predict(square_metres, car, distance, propertycount)[0]
    return {"predicted_price": round(price, 2)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)