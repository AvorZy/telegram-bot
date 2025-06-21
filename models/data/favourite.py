from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Favourite(BaseModel):
    id: int
    user_id: int
    car_id: Optional[int] = None
    accessory_id: Optional[int] = None
    saved_at: datetime

# Initialize empty list to store data
favourites = []
