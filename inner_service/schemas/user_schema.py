from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=79)
    last_name: str = Field(..., min_length=1, max_length=79)
    email: EmailStr = Field(...)


class UserRequest(UserBase):
    password: str = Field(..., min_length=8, max_length=63)


class UserResponse(UserBase):
    id_address: int = Field(..., gt=0)
    dropped: bool = Field(False)
