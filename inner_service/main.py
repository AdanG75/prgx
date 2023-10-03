from fastapi import FastAPI, Depends, Query, status
from sqlalchemy.orm import Session

from data.database import get_db
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
async def home(
        test: bool = Query(False),
        db: Session = Depends(get_db)
) -> dict:
    return {"directory": "home"}

