from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    id: int
    telegram_id: int
    first_name: Optional[str]
    last_name: Optional[str]
    username: Optional[str]
    phone_number: Optional[str]
    language: str = "en"
    is_first_time: bool = True
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
        
        print(f"User data initialization completed. Users loaded on-demand via API.")
        
    except Exception as e:
        print(f"Error initializing user data: {e}")
        # Keep empty list as fallback
        users = []

# Initialize user data when module is imported
initialize_user_data()z
