from pydantic import BaseModel, Field

# Class that is used for the API route 
# @app.post("/add-predicted-values/")
# this models what is sent through and needs to be saved to the CSV file 
class NewPredictedValues(BaseModel):
    Landsize: float = Field(..., gt=0, description="Square metres of the house")
    Distance: float = Field(..., description="Distance from CBD")
    Room: int = Field(..., gt=0, description="Number of rooms of property")
    Car: int = Field(..., description="Number of car parks on property")