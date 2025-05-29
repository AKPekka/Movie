"""Configuration settings for the movie recommendation app."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv("h.env")

# API Configuration
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Cache Configuration
CACHE_TTL = int(os.getenv("CACHE_TTL", 3600))  # Default: 1 hour
MAX_CACHE_SIZE = 1000  # Maximum number of items in cache

# App Configuration
DEBUG = os.getenv("FLASK_ENV") == "development"
