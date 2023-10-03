from fastapi import FastAPI

from route.address_router import router as address_router
from route.user_router import router as user_router

app = FastAPI()
app.include_router(router=address_router)
app.include_router(router=user_router)


@app.get("/")
async def home():
    return {"directory": "home"}

