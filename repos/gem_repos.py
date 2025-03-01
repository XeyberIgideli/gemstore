from sqlmodel import select
from api import deps
from models.gem_model import Gem,GemSpecification
from sqlalchemy.orm import joinedload, selectinload


def select_all_gems(db: deps.db):
    statement = select(Gem).options(joinedload(Gem.gem_specification)) 
    gems = db.exec(statement).all()   
    return gems

def select_gem (db:deps.db, id:int):
    gem = db.get(Gem, id) 
    return gem
    

def create_new_gem (db:deps.db, gem: Gem, gem_specs: GemSpecification):
    print(gem)