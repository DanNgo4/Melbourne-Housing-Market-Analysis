from pydantic import BaseModel, Field

class NewPredictedValues(BaseModel):
    Landsize: float = Field(..., gt=0, description="Square metres of the house")
    Distance: float = Field(..., description="Distance from CBD")
    Room: int = Field(..., gt=0, description="Number of rooms of property")
    Car: int = Field(..., description="Number of car parks on property")

 ##ADD REGEX Validation e.g
# regex=r"^[a-zA-Z ]+$"
#Add min and Max where necessary
#min_length=2, 
#max_length=50,

class QueryDetails(BaseModel):
    priceRange: str  = Field(..., gt=0, description="Price Range queried")
    houseType: str  = Field(..., gt=0, description="Specific house type queried")
    highlighted: list  = Field(..., gt=0, description="Highlighed list queried")