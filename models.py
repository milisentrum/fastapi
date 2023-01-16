from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum
#
#типизация данных помогает с анотированием в питоне. пример анотирования в ф-ии foo
from typing import Tuple, List, Optional, Union, Dict

class Gender(str, Enum):
    male = "male"
    female = "female"

class People(BaseModel):
    id: Optional[UUID] = str
    last_name: str
    gender: Gender
    value: int
    label: int

    def __getitem__(self: dict, key):
        return getattr(self, key)