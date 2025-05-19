from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    role: str  # mentor or mentee

class UserOut(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True