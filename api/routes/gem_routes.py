from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from models.gem_model import Gem, GemSpecification
from api import deps
from sqlmodel import select 
from repos import gem_repos
from schemas.gem_schema import GemSpecificationBase,GemCreate, GemRead, GemUpdate, GemPatch


router = APIRouter(
    prefix="/gems",
    tags=["gems"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[GemRead])
def get_all_gems(db: deps.db ): 
    gems = gem_repos.select_all_gems(db) 
    return gems

@router.get('/gem', response_model=GemRead)
def get_gem (id:int, db:deps.db):
    gem = gem_repos.select_gem(db, id)
    return gem

@router.post("/")
def create_gem (gem: GemCreate, gem_specs: GemSpecificationBase, db: deps.db): 
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
    
@router.put('/update',response_model=GemUpdate)
def update_gem (id:int, gem:GemUpdate, db:deps.db):
    gem_data = gem_repos.select_gem(db, id)
    
    if gem_data is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    
    gem_data.price = gem.price
    gem_data.type = gem.type
    gem_data.is_available = gem.is_available
    gem_data.gem_specification.clarity = gem.gem_specification.clarity
    gem_data.gem_specification.size = gem.gem_specification.size
    gem_data.gem_specification.color = gem.gem_specification.color
    
    
    db.add(gem_data)
    db.commit()
    db.refresh(gem_data)
    
    return gem

@router.patch('/patch', response_model=GemRead)
def patch_gem (id:int, db: deps.db, gem: GemPatch):
    db_gem = gem_repos.select_gem(db, id)
    
    if db_gem is None:
        raise HTTPException(status_code=404, detail="Gem not found")
    
    gem_data = gem.model_dump(exclude_unset=True)  
    
    for key, value in gem_data.items():
        setattr(db_gem, key, value)
    
    db.add(db_gem)
    db.commit()
    db.refresh(db_gem)
    
    return db_gem