from pydantic import BaseModel
from typing import List


class UserBase(BaseModel):
    username: str
    is_superuser: bool


class UserLoginCreate(UserBase):
    password: str
    is_superuser: bool = False


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class CurrencyBase(BaseModel):
    name: str


class Currency(CurrencyBase):
    id: int

    class Config:
        orm_mode = True


class MdBase(BaseModel):
    name: str


class Md(MdBase):
    id: int

    class Config:
        orm_mode = True


class StateBase(BaseModel):
    name: str


class State(StateBase):
    id: int

    class Config:
        orm_mode = True


class TypeBase(BaseModel):
    name: str


class Type(TypeBase):
    id: int

    class Config:
        orm_mode = True


class CoinsBase(BaseModel):
    description: str | None = None
    type_id: int
    currency_id: int
    nominal_value: str
    md_id: int
    state_id: int
    year: str | None = None
    serial_number: str
    user_id: int | None = None


class CoinResponse(BaseModel):
    id: int
    description: str
    type: Type
    currency: Currency
    nominal_value: str
    md: Md
    state: State
    year: str | None = None
    serial_number: str
    user: UserResponse

    class Config:
        orm_mode = True


class ListCoins(BaseModel):
    status: str
    results: int
    coins: List[CoinResponse]
