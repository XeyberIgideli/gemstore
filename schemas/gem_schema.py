from typing import Optional
from models.gem_model import Gem, GemSpecification, GemChoice, ClarityChoice, ColorChoice  # Replace with your actual module
from pydantic import BaseModel 

# Pydantic models for request body validation
class GemSpecificationBase(BaseModel):
    size: float
    clarity: ClarityChoice
    color: ColorChoice

class GemBase(BaseModel):
    price: float
    type: GemChoice
    is_available: bool = True
    gem_specification: GemSpecificationBase
    
class GemCreate(BaseModel):
    price: float
    type: GemChoice
    is_available: bool = True
    gem_specification: GemSpecificationBase

class GemRead(BaseModel):
    id: int
    price: float
    type: GemChoice
    is_available: bool
    gem_specification: GemSpecification    
     
class GemUpdate (GemBase): 
    is_available: bool   
    
class GemPatch (BaseModel):    
    price: Optional[float] = None
    type: Optional[GemChoice] = None
    is_available: Optional[bool] = None
    gem_specification: Optional[GemSpecificationBase] = None