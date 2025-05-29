"""Cache implementation for the movie recommendation app."""
from cachetools import TTLCache
from functools import wraps
import json
import hashlib
from config import CACHE_TTL, MAX_CACHE_SIZE

# Initialize cache with TTL and max size
cache = TTLCache(maxsize=MAX_CACHE_SIZE, ttl=CACHE_TTL)

def cache_key(*args, **kwargs):
    """Generate a cache key from function arguments."""
    key = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key.encode()).hexdigest()

def cached(func):
    """Decorator to cache function results."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = cache_key(func.__name__, *args, **kwargs)

        if key in cache:
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper

def clear_cache():
    """Clear the entire cache."""
    cache.clear()

def get_cache_stats():
    """Get cache statistics."""
    return {
        "size": len(cache),
        "maxsize": cache.maxsize,
        "ttl": cache.ttl,
        "currsize": cache.currsize
    }
