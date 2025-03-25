from pydantic import BaseModel, Field


class UserDataObj(BaseModel):
    email: str
    name: str


class GetUserInfoSchema(BaseModel):
    success: bool = Field(True)
    user: UserDataObj


class UserAuthSchema(GetUserInfoSchema):
    accessToken: str
    refreshToken: str


class UserErrorSchema(BaseModel):
    success: bool = Field(False)
    message: str
