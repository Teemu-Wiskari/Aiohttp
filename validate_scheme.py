import pydantic
import requests as requests
from typing import Optional
from settings import AIOHTTP_HOST, AIOHTTP_PORT

URL = f'http://{AIOHTTP_HOST}:{AIOHTTP_PORT}'


def err_short_password(password: str, min_lenght: int = 8) -> str:
    err = f"password short: less than {min_lenght} signs!"
    return err if len(password) < min_lenght else ''


def err_not_a_user(user_id: int) -> str:
    err = 'user not found...'
    response = requests.get(f'{URL}/user/{user_id}')
    return err if response.status_code != 200 else ''


class CreateUser(pydantic.BaseModel):

    username: str
    password: str
    email: Optional[str] = 'missing@email'

    @pydantic.field_validator('password')
    def validate_password(cls, value):

        error = err_short_password(value)
        if error:
            raise ValueError(error)

        return value


class PatchUser(pydantic.BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None

    @pydantic.field_validator('password')
    def validate_password(cls, value):
        error = err_short_password(value)
        if error:
            raise ValueError(error)
        return value


class CreateAd(pydantic.BaseModel):
    user_id: int
    header: Optional[str] = 'made ad'
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    def validate_user_id(cls, value):
        error = err_not_a_user(value)
        if error:
            raise ValueError(error)
        return value


class PatchAd(pydantic.BaseModel):
    user_id: Optional[int] = None
    header: Optional[str] = None
    description: Optional[str] = None

    @pydantic.field_validator('user_id')
    def validate_user_id(cls, value):
        error = err_not_a_user(value)
        if error:
            raise ValueError(error)
        return value
