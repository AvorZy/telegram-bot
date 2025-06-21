from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class Garage(BaseModel):
    """Model for garage data"""
    id: int
    garage_name: str
    location: str
    rating: float = 0.0
    phone_number: Optional[str] = None
    garage_service: str
    image_url: Optional[str] = None
    price_range: Optional[str] = None
    contact_info: Optional[str] = None
    operating_hours: Optional[str] = None
    user: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    map_link: Optional[str] = None
    distance_in_km: Optional[float] = None  # For nearby search functionality
    
    @classmethod
    def from_api_data(cls, data: dict) -> 'Garage':
        """Create Garage instance from API response data"""
        return cls(
            id=data.get('id'),
            garage_name=data.get('garageName', 'Unknown'),
            location=data.get('location', 'Unknown'),
            rating=data.get('rating', 0.0),
            phone_number=data.get('phoneNumber'),
            garage_service=data.get('garageService', 'Unknown'),
            image_url=data.get('imageUrl'),
            price_range=data.get('priceRange'),
            contact_info=data.get('contactInfo'),
            operating_hours=data.get('operatingHours'),
            user=data.get('user'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            map_link=data.get('mapLink')
        )
    
    def get_full_image_url(self, base_url: str = "https://pub-133f8593b35749f28fa090bc33925b31.r2.dev/") -> Optional[str]:
        """Get full image URL by combining base URL with image filename"""
        if self.image_url and not self.image_url.startswith(('http://', 'https://')):
            return f"{base_url}{self.image_url}"
        return self.image_url
    
    def get_rating_stars(self) -> str:
        """Get rating as star emojis"""
        full_stars = int(self.rating)
        half_star = 1 if self.rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_star
        
        return "⭐" * full_stars + "⭐" * half_star + "☆" * empty_stars
    
    def get_formatted_details(self, language: str = 'en', telegram_id: int = None) -> str:
        """Get formatted garage details for display"""
        from utils.ui.language import language_handler
        
        details = f"🏪 **{self.garage_name}**\n\n"
        
        details += f"{language_handler.get_text('garage_location', telegram_id).format(location=self.location)}\n"
        details += f"{language_handler.get_text('garage_rating', telegram_id).format(rating=self.rating)} {self.get_rating_stars()}\n"
        details += f"{language_handler.get_text('garage_service', telegram_id).format(service=self.garage_service)}\n"
        
        if self.price_range:
            details += f"{language_handler.get_text('garage_price_range', telegram_id).format(price_range=self.price_range)}\n"
        if self.phone_number:
            details += f"{language_handler.get_text('garage_phone', telegram_id).format(phone=self.phone_number)}\n"
        if self.contact_info:
            details += f"{language_handler.get_text('garage_contact', telegram_id).format(contact=self.contact_info)}\n"
        if self.operating_hours:
            details += f"{language_handler.get_text('garage_hours', telegram_id).format(hours=self.operating_hours)}\n"
        if self.map_link:
            details += f"[{language_handler.get_text('garage_map_link', telegram_id)}]({self.map_link})\n"
        
        return details