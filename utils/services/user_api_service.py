import os
import aiohttp
import asyncio
import os
from typing import Dict, Optional, List
from datetime import datetime
from utils.config.settings import API_BASE_URL

class UserAPIService:
    """Handles user management operations with external API"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.api_timeout = int(os.getenv('API_TIMEOUT', '30'))
    
    async def get_user(self, telegram_id: int) -> Optional[Dict]:
        """Get user data from API by telegram ID"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/User/GetTelegramUser/{telegram_id}",
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"DEBUG: Raw API response for user {telegram_id}: {data}")
                        
                        # The API returns user data directly, not wrapped in a 'data' field
                        user_data = data if isinstance(data, dict) and data.get('telegramId') else None
                        if user_data:
                            print(f"DEBUG: Extracted user data for {telegram_id}: {user_data}")
                            print(f"DEBUG: Language field from API for user {telegram_id}: {user_data.get('language', 'FIELD_NOT_FOUND')}")
                        else:
                            print(f"DEBUG: No valid user data found in response for {telegram_id}")
                        
                        return user_data
                    elif response.status == 404:
                        print(f"DEBUG: User {telegram_id} not found in API (404)")
                        return None
                    else:
                        print(f"DEBUG: API error for user {telegram_id}, status: {response.status}")
                        response.raise_for_status()
        except Exception as e:
            pass
            return None
    
    async def create_user(self, user_data: Dict) -> Optional[Dict]:
        """Create new user via API"""
        try:
            # Prepare user data for API - matching new route structure
            api_user_data = {
                "telegramId": user_data.get('telegramId'),
                "username": user_data.get('username', ''),
                "firstName": user_data.get('firstName', ''),
                "lastName": user_data.get('lastName', ''),
                "language": user_data.get('language', 'en')
            }
            
            print(f"DEBUG: Creating user with data: {api_user_data}")
            print(f"DEBUG: Language being sent to API: {api_user_data.get('language')}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/User/CreateTelegramUser",
                    json=api_user_data,
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    if response.status in [200, 201]:
                        data = await response.json()
                        print(f"DEBUG: Create user API response: {data}")
                        
                        created_user = data.get('data') if isinstance(data, dict) else data
                        if created_user:
                            print(f"DEBUG: Created user data: {created_user}")
                            print(f"DEBUG: Language field in created user: {created_user.get('language', 'FIELD_NOT_FOUND')}")
                        
                        return created_user
                    elif response.status == 409:
                        # User already exists, return None to trigger get_user in get_or_create_user
                        print(f"User {user_data.get('telegram_id')} already exists (409 Conflict)")
                        return None
                    else:
                        response.raise_for_status()
        except Exception as e:
            pass
            return None
    
    async def update_user(self, telegram_id: int, update_data: Dict) -> Optional[Dict]:
        """Update user data via API"""
        try:
            # Prepare update data for API
            api_update_data = {
                "language": update_data.get('language'),
                "settings": update_data.get('settings'),
                "latitude": update_data.get('latitude'),
                "longitude": update_data.get('longitude'),
                "locationUpdatedAt": update_data.get('locationUpdatedAt')
            }
            
            # Remove None values
            api_update_data = {k: v for k, v in api_update_data.items() if v is not None}
            
            pass
            if 'language' in api_update_data:
                pass
            
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.api_base_url}/User/UpdateTelegramUser/{telegram_id}",
                    json=api_update_data,
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"DEBUG: Update user API response: {data}")
                        
                        # The API returns the user object directly, not wrapped in 'data'
                        updated_user = data if isinstance(data, dict) and data.get('telegramId') else None
                        if updated_user:
                            print(f"DEBUG: Updated user data: {updated_user}")
                            print(f"DEBUG: Language field in updated user: {updated_user.get('language', 'FIELD_NOT_FOUND')}")
                        else:
                            print(f"DEBUG: No valid user data found in API response")
                        
                        return updated_user
                    else:
                        print(f"DEBUG: API update failed for user {telegram_id}, status: {response.status}")
                        response.raise_for_status()
        except Exception as e:
            pass
            return None
    
    async def get_user_favorites(self, telegram_id: int) -> List[Dict]:
        """Get user's favorite cars from API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/User/{telegram_id}/favorites",
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', []) if isinstance(data, dict) else data
                    elif response.status == 404:
                        return []
                    else:
                        response.raise_for_status()
        except Exception as e:
            pass
            return []
    
    async def add_favorite(self, telegram_id: int, car_id: int) -> bool:
        """Add car to user's favorites via API"""
        try:
            favorite_data = {
                "telegramId": telegram_id,
                "carId": car_id,
                "addedAt": datetime.now().isoformat()
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_base_url}/User/{telegram_id}/favorites",
                    json=favorite_data,
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    return response.status in [200, 201]
        except Exception as e:
            pass
            return False
    
    async def remove_favorite(self, telegram_id: int, car_id: int) -> bool:
        """Remove car from user's favorites via API"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.delete(
                    f"{self.api_base_url}/User/{telegram_id}/favorites/{car_id}",
                    timeout=aiohttp.ClientTimeout(total=self.api_timeout)
                ) as response:
                    return response.status in [200, 204]
        except Exception as e:
            pass
            return False
    
    async def update_user_location(self, telegram_id: int, latitude: float, longitude: float) -> bool:
        """Update user's location coordinates"""
        try:
            from datetime import datetime
            location_data = {
                'latitude': latitude,
                'longitude': longitude,
                'locationUpdatedAt': datetime.now().isoformat()
            }
            
            print(f"DEBUG: Sending location data to API: {location_data}")
            updated_user = await self.update_user(telegram_id, location_data)
            print(f"DEBUG: API returned user data: {updated_user}")
            
            # Consider it successful if we get any user data back (API accepts the update)
            # The API might not return the location fields in the response
            success = updated_user is not None and updated_user.get('telegramId') == str(telegram_id)
            print(f"DEBUG: Location update success determination: {success}")
            return success
        except Exception as e:
            pass
            return False
    
    async def get_user_location(self, telegram_id: int) -> tuple[float, float] | None:
        """Get user's stored location coordinates"""
        try:
            user = await self.get_user(telegram_id)
            if user and user.get('latitude') and user.get('longitude'):
                return (user['latitude'], user['longitude'])
            return None
        except Exception as e:
            pass
            return None
    
    async def get_or_create_user(self, telegram_user) -> Dict:
        """Get existing user or create new one with dynamic language detection"""
        telegram_id = telegram_user.id
        
        # Try to get existing user first
        user = await self.get_user(telegram_id)
        
        if user:
            # For existing users, check if Telegram language has changed
            current_language = user.get('language', 'en')
            telegram_language = getattr(telegram_user, 'language_code', None)
            
            # Map Telegram language codes to supported languages
            detected_language = 'en'  # default
            if telegram_language:
                if telegram_language.startswith('km'):
                    detected_language = 'kh'
                elif telegram_language.startswith('en'):
                    detected_language = 'en'
            
            print(f"DEBUG: Existing user {telegram_id} - current: {current_language}, telegram: {telegram_language}, detected: {detected_language}")
            
            # Update language if it has changed and is different from current
            if detected_language != current_language:
                print(f"DEBUG: Language mismatch detected for user {telegram_id}. Updating from {current_language} to {detected_language}")
                updated_user = await self.update_user(telegram_id, {'language': detected_language})
                if updated_user:
                    return self._convert_api_user_to_local(updated_user)
            
            return self._convert_api_user_to_local(user)
        
        # User doesn't exist, create new user
        # Use telegram user's language_code if available, otherwise default to 'en'
        telegram_language = getattr(telegram_user, 'language_code', 'en') or 'en'
        
        # Map Telegram language codes to supported languages
        user_language = 'en'  # default
        if telegram_language.startswith('km'):
            user_language = 'kh'
        elif telegram_language.startswith('en'):
            user_language = 'en'
        
        print(f"DEBUG: Creating new user {telegram_user.id} - telegram language: {telegram_language}, mapped to: {user_language}")
        
        user_data = {
                'telegramId': str(telegram_user.id),
                'username': telegram_user.username,
                'firstName': telegram_user.first_name,
                'lastName': telegram_user.last_name,
                'language': user_language
            }
        
        created_user = await self.create_user(user_data)
        
        if created_user:
            return self._convert_api_user_to_local(created_user)
        
        # If creation failed, it might be due to race condition (user created between get and create)
        # Try to get user one more time
        user = await self.get_user(telegram_id)
        if user:
            return self._convert_api_user_to_local(user)
        
        # Fallback to local user if API fails completely
        # Use telegram user's language_code if available, otherwise default to 'en'
        telegram_language = getattr(telegram_user, 'language_code', 'en') or 'en'
        
        # Map Telegram language codes to supported languages
        fallback_language = 'en'  # default
        if telegram_language.startswith('km'):
            fallback_language = 'kh'
        elif telegram_language.startswith('en'):
            fallback_language = 'en'
        
        print(f"DEBUG: Fallback user {telegram_id} - telegram language: {telegram_language}, mapped to: {fallback_language}")
        
        return {
            'telegram_id': telegram_id,
            'first_name': telegram_user.first_name or '',
            'last_name': telegram_user.last_name or '',
            'username': telegram_user.username or '',
            'language': fallback_language,
            'source': 'local_fallback'
        }
    
    def _convert_api_user_to_local(self, api_user: Dict) -> Dict:
        """Convert API user format to local format"""
        # Handle both old and new API response formats
        first_name = api_user.get('firstName', '')
        last_name = api_user.get('lastName', '')
        
        # Fallback to name field if firstName/lastName not available
        if not first_name and not last_name:
            name = api_user.get('name', '')
            name_parts = name.split(' ', 1) if name else ['', '']
            first_name = name_parts[0] if len(name_parts) > 0 else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        # Convert telegramId from string to int
        telegram_id = api_user.get('telegramId')
        if isinstance(telegram_id, str):
            telegram_id = int(telegram_id)
        
        # Handle language - if not provided in API response, use 'en' as default
        # The language should be properly set through user settings or API
        language = api_user.get('language', 'en')
        
        print(f"DEBUG: Converting API user data - telegramId: {api_user.get('telegramId')}, language: {language}")
        
        return {
            'telegram_id': telegram_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': api_user.get('username', ''),
            'language': language,
            'is_active': api_user.get('isActive', True),
            'created_at': api_user.get('createdAt'),
            'updated_at': api_user.get('updatedAt'),
            'source': 'api'
        }

# Global instance
user_api_service = UserAPIService()