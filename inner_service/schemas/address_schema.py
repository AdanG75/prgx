from typing import Optional

from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    address_1: str = Field(..., min_length=4, max_length=79)
    address_2: Optional[str] = Field(None, min_length=1, max_length=79)
    city: Optional[str] = Field(None, min_length=1, max_length=79)
    state: str = Field(..., min_length=1, max_length=79)
    zip_code: str = Field(..., min_length=4, max_length=8)
    country: str = Field(..., min_length=2, max_length=49)


class AddressRequest(AddressBase):
    pass


class AddressResponse(AddressBase):
    id_address: int = Field(..., gt=0)
    dropped: bool = Field(False)
