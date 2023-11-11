import datetime
from typing import List, Union, Optional
from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str

    #wonGames: List['Game'] = []

    class Config:
        orm_mode = True


class UserData(User):
    id: int
    played_games: int
    signup_date: datetime.date
    disabled: bool
    admin: bool


class UserInDb(User):
    hashed_password: str


class Game(BaseModel):
    game_mode: int
    time: datetime.time
    errors: int
    hint: int
    player_id: int

    class Config:
        orm_mode = True


class GameInDb(Game):
    id: Optional[int]
    game_date: Optional[datetime.date]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
