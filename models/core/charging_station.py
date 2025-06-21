from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class ChargingStation(BaseModel):
    """Model for charging station data"""
    id: int
    name: str
    type: str
    capacity: Optional[str] = None
    power_value: int
    price_per_kwh: float
    phone_number: Optional[str] = None
    distance_in_km: float
    rating: float = 0.0
    availability: bool = True
    location: str
    map_link: Optional[str] = None
    connector_types: List[str] = []
    image_url: Optional[str] = None
    
    @classmethod
    def from_api_data(cls, data: dict) -> 'ChargingStation':
        """Create ChargingStation instance from API response data"""
        return cls(
            id=data.get('id'),
            name=data.get('name', 'Unknown'),
            type=data.get('type', 'Unknown'),
            capacity=data.get('capacity'),
            power_value=data.get('powerValue', 0),
            price_per_kwh=data.get('pricePerKwh', 0.0),
            phone_number=data.get('phoneNumber'),
            distance_in_km=data.get('distanceInKm', 0.0),
            rating=data.get('rating', 0.0),
            availability=data.get('availability', True),
            location=data.get('location', 'Unknown'),
            map_link=data.get('mapLink'),
            connector_types=data.get('connectorTypes', []),
            image_url=data.get('imageUrl')
        )
    
    def get_full_image_url(self, base_url: str = "https://inventoryapiv1-367404119922.asia-southeast1.run.app/uploads/") -> str:
        """Get full image URL by combining base URL with image filename"""
        if not self.image_url:
            return ""
        if not self.image_url.startswith(('http://', 'https://')):
            return f"{base_url}{self.image_url}"
        return self.image_url
    
    def get_availability_text(self, language: str = 'en') -> str:
        """Get availability status text in specified language"""
        if language == 'en':
            return "✅ Available" if self.availability else "❌ Closed"
        else:
            return "✅ មាន" if self.availability else "❌ បានបិទ"
    
    def get_formatted_details(self, language: str = 'en') -> str:
        """Get formatted station details for display"""
        connectors = ', '.join(self.connector_types) if self.connector_types else 'N/A'
        availability_text = self.get_availability_text(language)
        
        if language == 'en':
            return f"""🔌 {self.name}

📍 Location: {self.location}
⚡ Type: {self.type} ({self.power_value}kW)
💰 Price: ${self.price_per_kwh}/kWh
📏 Distance: {self.distance_in_km}km
🔌 Connectors: {connectors}
📞 Phone: {self.phone_number or 'N/A'}
🟢 Status: {availability_text}"""
        else:
            return f"""🔌 **{self.name}**

📍 ទីតាំង: {self.location}
⚡ ប្រភេទ: {self.type} ({self.power_value}kW)
💰 តម្លៃ: ${self.price_per_kwh}/kWh
📏 ចម្ងាយ: {self.distance_in_km}km
🔌 ប្រភេទសាក: {connectors}
📞 ទូរស័ព្ទ: {self.phone_number or 'N/A'}
🟢 ស្ថានភាព: {availability_text}"""