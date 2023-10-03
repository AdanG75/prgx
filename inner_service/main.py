from fastapi import FastAPI, status

from route.address_router import router as address_router
from route.user_router import router as user_router

app = FastAPI(title="PRGX-Inner-Service", version="0.1.0")
app.include_router(router=address_router)
app.include_router(router=user_router)


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home of application"
)
async def home() -> dict:
    return {"directory": "home"}

