import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging based on environment
log_level = getattr(logging, os.getenv('LOG_LEVEL', 'INFO').upper())
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Bot Configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Environment Configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

# Validation
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is required")

if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID environment variable is required")

# Environment-specific settings
if ENVIRONMENT == 'production':
    DEBUG = False
    LOG_LEVEL = 'WARNING'
elif ENVIRONMENT == 'staging':
    DEBUG = True
    LOG_LEVEL = 'INFO'
else:  # development
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://inventoryapiv1-367404119922.asia-southeast1.run.app')
API_BASE_URL_IMG = os.getenv('API_BASE_URL', 'https://pub-133f8593b35749f28fa090bc33925b31.r2.dev')



print(f"Running in {ENVIRONMENT} environment")
print(f"API Base URL: {API_BASE_URL}")