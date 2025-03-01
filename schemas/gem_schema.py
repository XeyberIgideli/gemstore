from models.gem_model import Gem, GemSpecification, GemChoice, ClarityChoice, ColorChoice  # Replace with your actual module
from pydantic import BaseModel 

# Pydantic models for request body validation
class GemSpecificationCreate(BaseModel):
    size: float
    clarity: ClarityChoice
    color: ColorChoice

class GemCreate(BaseModel):
    price: float
    type: GemChoice
    is_available: bool = True
    gem_specification: GemSpecificationCreate

class GemRead(BaseModel):
    id: int
    price: float
    type: GemChoice
    is_available: bool
    gem_specification: GemSpecification    