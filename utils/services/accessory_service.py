import asyncio
import aiohttp
import os
from typing import List, Optional, Dict, Any
from models.core.accessory import Accessory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AccessoryService:
    """Service for handling accessory data from API"""
    
    def __init__(self):
        self.base_url = os.getenv('API_BASE_URL', "https://inventoryapiv1-367404119922.asia-southeast1.run.app")
        # Use environment variables like data_loader
        self.image_base_url = os.getenv('API_BASE_URL_IMG', "https://inventoryapiv1-367404119922.asia-southeast1.run.app/uploads/")
        r2_base = os.getenv('API_BASE_URL_IMG', "https://pub-133f8593b35749f28fa090bc33925b31.r2.dev")
        self.r2_image_base_url = r2_base if r2_base.endswith('/') else f"{r2_base}/"
        self.accessories_cache = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5 minutes
        
    async def fetch_all_accessories(self) -> List[Accessory]:
        """Fetch all accessories from API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/Accessory") as response:
                    if response.status == 200:
                        data = await response.json()
                        accessories_data = data.get('data', [])
                        return [Accessory.from_api_data(acc_data) for acc_data in accessories_data]
                    else:
                        print(f"Error fetching accessories: HTTP {response.status}")
                        return []
        except Exception as e:
            print(f"Error fetching accessories: {e}")
            return []
    
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
        """Get full image URL from filename with validation - supports both API and R2 storage"""
        if not image_filename:
            return ""
        
        # Clean the image filename (strip whitespace and trailing commas)
        cleaned_filename = image_filename.strip().rstrip(',')
        
        # If already a full URL, validate and return it
        if cleaned_filename.startswith(('http://', 'https://')):
            # Basic URL validation
            if '.' in cleaned_filename and len(cleaned_filename) > 10:
                # Test if the URL is accessible
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.head(cleaned_filename, timeout=aiohttp.ClientTimeout(total=3)) as response:
                            if response.status == 200:
                                return cleaned_filename
                except Exception:
                    pass
            return ""
        
        # Try R2 storage first (newer images) and validate
        r2_url = f"{self.r2_image_base_url}{cleaned_filename}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(r2_url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        return r2_url
        except Exception:
            pass
        
        # Try API storage as fallback and validate
        api_url = f"{self.image_base_url}{cleaned_filename}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(api_url, timeout=aiohttp.ClientTimeout(total=3)) as response:
                    if response.status == 200:
                        return api_url
        except Exception:
            pass
        
        return ""
    
    def get_fallback_image_url(self, image_filename: str) -> str:
        """Get fallback image URL from original API storage"""
        if not image_filename:
            return ""
        
        if image_filename.startswith(('http://', 'https://')):
            return image_filename
            
        return f"{self.image_base_url}{image_filename}"