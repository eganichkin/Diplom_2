from typing import List
from pydantic import BaseModel, Field


class OrderIngredientObj(BaseModel):
    id: str = Field(alias="_id")
    name: str
    type: str
    proteins: int
    fat: float
    carbohydrates: float
    calories: int
    price: float
    image: str
    image_mobile: str
    image_large: str
    v: int = Field(alias="__v")


class OrderOwnerObj(BaseModel):
    name: str
    email: str
    createdAt: str
    updatedAt: str


class OrderDataObj(BaseModel):
    ingredients: List[OrderIngredientObj]
    id: str = Field(alias="_id")
    owner: OrderOwnerObj
    status: str = Field("done")
    name: str
    createdAt: str
    updatedAt: str
    number: int
    price: float


class GetOrderInfoSchema(BaseModel):
    success: bool
    name: str
    order: OrderDataObj


class OrderDataWithoutAuthObj(BaseModel):
    number: int


class GetOrderInfoWithoutAuthSchema(BaseModel):
    success: bool = Field(True)
    name: str
    order: OrderDataWithoutAuthObj


class OrderErrorSchema(BaseModel):
    success: bool = Field(False)
    message: str


class UserOrdersDataObj(BaseModel):
    id: str = Field(alias="_id")
    ingredients: List[str]
    status: str
    createdAt: str
    updatedAt: str
    number: int


class UserOrdersSchema(BaseModel):
    success: bool = Field(True)
    orders: List[UserOrdersDataObj]
    total: int
    totalToday: int
