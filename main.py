from fastapi import FastAPI
from  core.db import init_db
import uvicorn 
from api.routes.gem_routes import router
 
app = FastAPI()

# Gems Router
app.include_router(router)

# @app.on_event("startup")
# async def on_startup():
#     init_db()
 
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)