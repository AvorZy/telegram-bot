from typing import List, Optional, Dict, Any
from utils.ui.language import language_handler

class Accessory:
    """Accessory model for EV accessories"""
    
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        image: Optional[str],
        price: float,
        phone_number: str,
        rating: float,
        review_count: int,
        weight: Optional[float],
        color: Optional[str],
        category_id: int,
        category: str,
        brand_id: int,
        brand: str,
        location: str,
        sku: str,
        compatible_models: List[str]
    ):
        self.id = id
        self.name = name
        self.description = description
        self.image = image
        self.price = price
        self.phone_number = phone_number
        self.rating = rating
        self.review_count = review_count
        self.weight = weight
        self.color = color
        self.category_id = category_id
        self.category = category
        self.brand_id = brand_id
        self.brand = brand
        self.location = location
        self.sku = sku
        self.compatible_models = compatible_models
        # Keep type as category for backward compatibility
        self.type = category
    
    @classmethod
    def from_api_data(cls, data: Dict[str, Any]) -> 'Accessory':
        """Create Accessory instance from API data"""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            description=data.get('description', ''),
            image=data.get('image'),
            price=data.get('price', 0),
            phone_number=data.get('phoneNumber', 'Not specified'),
            rating=data.get('rating', 0.0),
            review_count=data.get('reviewCount', 0),
            weight=data.get('weight'),
            color=data.get('color'),
            category_id=data.get('categoryId', 0),
            category=data.get('category', ''),
            brand_id=data.get('brandId', 0),
            brand=data.get('brand', ''),
            location=data.get('location', ''),
            sku=data.get('sku', ''),
            compatible_models=data.get('compatibleModels', [])
        )
    
    def get_full_image_url(self, base_url: str = None) -> str:
        """Get full image URL by combining base URL with image filename"""
        import os
        
        if not self.image:
            return ""
            
        # If already a full URL, return as is
        if self.image.startswith(('http://', 'https://')):
            return self.image
            
        # If it's just a filename, combine with base URL
        if self.image.strip():
            # Use environment variable or provided base_url or default
            if base_url is None:
                base_url = os.getenv('API_BASE_URL_IMG', "https://pub-133f8593b35749f28fa090bc33925b31.r2.dev")
            
            # Ensure base URL ends with slash
            if not base_url.endswith('/'):
                base_url += '/'
            return f"{base_url}{self.image.strip()}"
            
        return ""
    
    def get_formatted_details(self, user_language: str = 'en', telegram_id: int = None) -> str:
        """Get formatted accessory details for display"""
        
        # Format rating stars
        stars = "⭐" * int(self.rating)
        if self.rating % 1 >= 0.5:
            stars += "⭐"
        
        # Build details string with translations
        details = f"🔧 {self.name}\n"
        details += f"📝 {self.description}\n\n"
        details += f"💰 ${self.price:,.2f}\n"
        details += f"📞 {self.phone_number}\n"
        details += f"🏷️ {self.category} ({self.brand})\n"
        details += f"⭐ {self.rating}/5 ({self.review_count} reviews) {stars}\n"
        details += f"📍 {self.location}\n"
        details += f"🏷️ SKU: {self.sku}\n"
        
        if self.weight:
            details += f"⚖️ Weight: {self.weight}kg\n"
        
        if self.color:
            details += f"🎨 Color: {self.color}\n"
        
        if self.compatible_models and self.compatible_models != ['None']:
            details += f"🚗 Compatible: {', '.join(self.compatible_models)}\n"
        
        return details