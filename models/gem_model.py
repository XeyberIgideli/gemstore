from sqlmodel import SQLModel, Field, Relationship, Column
from typing import List,Optional
import sqlalchemy as sa
from enum import Enum


class GemChoice(str, Enum):
    RUBY = "ruby"
    DIAMOND = "diamond"
    EMERALD = "emerald"
    SAPPHIRE = "sapphire"
    AMETHYST = "amethyst"
    TOPAZ = "topaz"
     

class ClarityChoice(str, Enum):
    FL = "fl"      # Flawless
    IF = "if"      # Internally Flawless
    VVS = "vvs"    # Very Very Slightly Included
    VS = "vs"      # Very Slightly Included
    SI = "si"      # Slightly Included
    I = "i"        # Included
     
class ColorChoice(str, Enum):
    D = "d"        # Colorless
    E = "e"        # Colorless
    F = "f"        # Colorless
    G = "g"        # Near Colorless
    H = "h"        # Near Colorless
    I = "i"        # Near Colorless
    J = "j"        # Near Colorless
    K = "k"        # Faint Color
 
class GemSpecification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True) 
    size: float = 1  
    clarity: ClarityChoice = Field(sa_column=Column(sa.Enum(ClarityChoice, native_enum=False))) # sa_column is used to specify the column name
    color: ColorChoice = Field(sa_column=Column(sa.Enum(ColorChoice, native_enum=False)))
    gem: Optional['Gem'] = Relationship(back_populates="gem_specification") # Why List["Gem"]? Because it's a many-to-one relationship
    
class Gem(SQLModel, table=True):  
    id: Optional[int] = Field(default=None, primary_key=True)
    price: float
    type: GemChoice = Field(sa_column=Column(sa.Enum(GemChoice))) 
    is_available: bool = True
    gem_specification_id: Optional[int] = Field(default=None, foreign_key="gemspecification.id")
    gem_specification: Optional[GemSpecification] = Relationship(back_populates="gem") 
    # seller_id: int = Field(default=None, foreign_key="user.id")