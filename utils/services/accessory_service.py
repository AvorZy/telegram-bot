import asyncio
import aiohttp
import os
import time
from typing import List, Optional, Dict, Any
from models.core.accessory import Accessory
from utils.config.settings import API_BASE_URL, API_BASE_URL_IMG

class AccessoryService:
    """Service for handling accessory data from API"""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        # Use environment variables like data_loader
        self.image_base_url = API_BASE_URL_IMG
        self.r2_image_base_url = API_BASE_URL_IMG if API_BASE_URL_IMG.endswith('/') else f"{API_BASE_URL_IMG}/"
        self.accessories_cache = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
        # Image URL validation cache
        self.image_url_cache = {}
        self.image_cache_duration = 1800  # 30 minutes
        
    async def fetch_all_accessories(self) -> List[Accessory]:
        """Fetch all accessories from API with caching"""
        current_time = time.time()
        
        # Check if cache is still valid
        if (self.accessories_cache and 
            current_time - self.cache_timestamp < self.cache_duration):
            pass
            return self.accessories_cache
        
        # Fetch fresh data from API
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/Accessory") as response:
                    if response.status == 200:
                        data = await response.json()
                        accessories_data = data.get('data', [])
                        self.accessories_cache = [Accessory.from_api_data(acc_data) for acc_data in accessories_data]
                        self.cache_timestamp = current_time
                        pass
                        return self.accessories_cache
                    else:
                        pass
                        return self.accessories_cache if self.accessories_cache else []
        except Exception as e:
            pass
            return self.accessories_cache if self.accessories_cache else []
    
    async def get_unique_types(self) -> List[str]:
        """Get unique accessory categories"""
        accessories = await self.fetch_all_accessories()
        categories = list(set(acc.category for acc in accessories if acc.category))
        return sorted(categories)
    
    async def get_unique_brands(self) -> List[str]:
        """Get unique accessory brands"""
        accessories = await self.fetch_all_accessories()
        brands = list(set(acc.brand for acc in accessories if acc.brand))
        return sorted(brands)
    
    async def get_unique_colors(self) -> List[str]:
        """Get unique accessory colors"""
        accessories = await self.fetch_all_accessories()
        colors = list(set(acc.color for acc in accessories if acc.color))
        return sorted(colors)
    
    async def get_unique_locations(self) -> List[str]:
        """Get unique accessory locations"""
        accessories = await self.fetch_all_accessories()
        locations = list(set(acc.location for acc in accessories if acc.location))
        return sorted(locations)
    
    async def get_accessories_by_type(self, accessory_type: str) -> List[Accessory]:
        """Get accessories filtered by category"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.category == accessory_type]
    
    async def get_accessories_by_brand(self, brand: str) -> List[Accessory]:
        """Get accessories filtered by brand"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.brand == brand]
    
    async def get_accessories_by_color(self, color: str) -> List[Accessory]:
        """Get accessories filtered by color"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.color == color]
    
    async def get_accessories_by_price_range(self, min_price: float, max_price: float) -> List[Accessory]:
        """Get accessories filtered by price range"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if min_price <= acc.price <= max_price]
    
    async def get_accessories_by_location(self, location: str) -> List[Accessory]:
        """Get accessories filtered by location"""
        accessories = await self.fetch_all_accessories()
        return [acc for acc in accessories if acc.location == location]
    
    async def fetch_accessory_by_id(self, accessory_id: int) -> Optional[Accessory]:
        """Get specific accessory by ID from API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/Accessory/{accessory_id}") as response:
                    if response.status == 200:
                        data = await response.json()
                        return Accessory.from_api_data(data)
                    else:
                        print(f"Error fetching accessory {accessory_id}: HTTP {response.status}")
                        return None
        except Exception as e:
            print(f"Error fetching accessory {accessory_id}: {e}")
            return None
    
    async def get_accessory_by_id(self, accessory_id: int) -> Optional[Accessory]:
        """Get specific accessory by ID (fallback to list search)"""
        # Try direct API call first
        accessory = await self.fetch_accessory_by_id(accessory_id)
        if accessory:
            return accessory
        
        # Fallback to searching in the full list
        accessories = await self.fetch_all_accessories()
        for acc in accessories:
            if acc.id == accessory_id:
                return acc
        return None
    
    async def search_accessories(self, query: str = None, category: str = None, brand: str = None, 
                                color: str = None, min_price: float = None, max_price: float = None) -> List[Accessory]:
        """Search accessories with multiple filters"""
        accessories = await self.fetch_all_accessories()
        
        # Apply text search filter
        if query:
            query_lower = query.lower()
            accessories = [
                acc for acc in accessories 
                if query_lower in acc.name.lower() or query_lower in acc.description.lower()
            ]
        
        # Apply category filter
        if category:
            accessories = [acc for acc in accessories if acc.category == category]
        
        # Apply brand filter
        if brand:
            accessories = [acc for acc in accessories if acc.brand == brand]
        
        # Apply color filter
        if color:
            accessories = [acc for acc in accessories if acc.color == color]
        
        # Apply price range filter
        if min_price is not None:
            accessories = [acc for acc in accessories if acc.price >= min_price]
        
        if max_price is not None:
            accessories = [acc for acc in accessories if acc.price <= max_price]
        
        return accessories
    
    async def get_full_image_url(self, image_filename: str) -> str:
        """Get full image URL from filename with cached validation - supports both API and R2 storage"""
        if not image_filename:
            return ""
        
        # Clean the image filename (strip whitespace and trailing commas)
        cleaned_filename = image_filename.strip().rstrip(',')
        
        # Check cache first
        current_time = time.time()
        cache_key = cleaned_filename
        if cache_key in self.image_url_cache:
            cached_result, cached_time = self.image_url_cache[cache_key]
            if current_time - cached_time < self.image_cache_duration:
                return cached_result
        
        # If already a full URL, do basic validation and return it
        if cleaned_filename.startswith(('http://', 'https://')):
            if '.' in cleaned_filename and len(cleaned_filename) > 10:
                self.image_url_cache[cache_key] = (cleaned_filename, current_time)
                return cleaned_filename
            self.image_url_cache[cache_key] = ("", current_time)
            return ""
        
        # Try R2 storage first (newer images) - assume it works to avoid HTTP calls
        r2_url = f"{self.r2_image_base_url}{cleaned_filename}"
        # Cache and return R2 URL without validation for performance
        self.image_url_cache[cache_key] = (r2_url, current_time)
        return r2_url
    
    def get_fallback_image_url(self, image_filename: str) -> str:
        """Get fallback image URL from original API storage"""
        if not image_filename:
            return ""
        
        if image_filename.startswith(('http://', 'https://')):
            return image_filename
            
        return f"{self.image_base_url}{image_filename}"