from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from core.db import get_db

db = Annotated[Session, Depends(get_db)]