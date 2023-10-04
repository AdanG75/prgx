from pydantic import BaseModel, Field


class UserAddressResponse(BaseModel):
    id_user: int = Field(..., gt=0)
    id_address: int = Field(..., gt=0)
    valid: bool = Field(...)

    model_config = {
        "from_attributes": True
    }
