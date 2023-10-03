from fastapi import FastAPI

from routes.address_router import router as address_router
from routes.health_router import route as health_router
from routes.user_router import router as user_router

app = FastAPI()
app.include_router(router=address_router)
app.include_router(router=health_router)
app.include_router(router=user_router)


@app.get("/", tags=["Home"])
async def hello():
    return {"Greetings": "Hello world"}

