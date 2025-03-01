from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from models.gem_model import Gem, GemSpecification
from api import deps
from sqlmodel import select, delete, col, func 
from repos import gem_repos
from schemas.gem_schema import GemSpecificationCreate,GemCreate, GemRead


router = APIRouter(
    prefix="/gems",
    tags=["gems"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[GemRead])
def get_all_gems(db: deps.db ): 
    gems = gem_repos.select_all_gems(db)
    return gems

@router.post("/")
def create_gem (gem: GemCreate, gem_specs: GemSpecificationCreate, db: deps.db): 
   try:
        new_gem_specs = GemSpecification(clarity=gem_specs.clarity.value, size=gem_specs.size,color=gem_specs.color.value)  
     
        db.add(new_gem_specs)
        db.commit()
        db.refresh(new_gem_specs)
        
        new_gem = Gem(price=gem.price, is_available=gem.is_available, type=gem.type, gem_specification_id=new_gem_specs.id,
                      gem_specification=new_gem_specs)
        db.add(new_gem)
        db.commit() 
        return {"gem": gem, "gem_specification": gem_specs}
   except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))