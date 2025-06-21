from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    id: int
    user_id: int
    message: str
    direction: str
    timestamp: datetime

# Initialize empty list to store data
messages = []
