from sqlmodel import Session, SQLModel, create_engine 

DATABASE_URL = 'sqlite:///./gemstore.db'

engine = create_engine(DATABASE_URL, echo=True)

def get_db ():
    db = Session(bind=engine)
    
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e  # Re-raise the exception
    finally:
        db.close() 
        
def init_db ():
    SQLModel.metadata.drop_all(bind=engine) 
    SQLModel.metadata.create_all(bind=engine)        