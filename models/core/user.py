from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    id: int
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    language: str = "en"
    is_first_time: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_updated_at: Optional[datetime] = None
    created_at: datetime

# Initialize empty list to store data
users = []

# Import user_api_service for data loading
from utils.services.user_api_service import user_api_service

def initialize_user_data():
    """Initialize user data from API service"""
    global users
    try:
        # Clear existing users
        users.clear()
        
        # Note: Users are loaded dynamically via API calls when needed
        # This function is kept for consistency with product.py structure
        # but users are typically loaded on-demand via get_or_create_user
        
        pass
        
    except Exception as e:
        pass
        # Keep empty list as fallback
        users = []

# Initialize user data when module is imported
initialize_user_data()