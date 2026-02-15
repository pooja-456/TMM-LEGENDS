from pydantic import BaseModel
from typing import List, Optional


class Legend(BaseModel):
    NAME: str
    GENDER: str
    CITY: str
    STATE: str
    NO_OF_MARATHONS: Optional[int]
    STARS: str
    YEAR: int


class LegendsResponse(BaseModel):
    file: Optional[str]
    total: int
    data: List[Legend]
