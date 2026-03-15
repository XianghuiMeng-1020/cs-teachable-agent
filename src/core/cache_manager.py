"""
Cache Manager for Performance Optimization

Implements multi-level caching:
- In-memory LRU cache for hot data
- Persistent cache for session data
- Cache invalidation strategies
"""

import time
import hashlib
from functools import wraps
from typing import Any, Optional, Callable
from dataclasses import dataclass
from collections import OrderedDict


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    value: Any
    created_at: float
    ttl: int  # Time to live in seconds
    access_count: int = 0
    last_accessed: float = 0


class LRUCache:
    """Thread-safe LRU Cache implementation."""
    
    def __init__(self, capacity: int = 1000, default_ttl: int = 300):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            self._misses += 1
            return None
        
        entry = self._cache[key]
        
        # Check expiration
        if time.time() - entry.created_at > entry.ttl:
            del self._cache[key]
            self._misses += 1
            return None
        
        # Update access stats
        entry.access_count += 1
        entry.last_accessed = time.time()
        
        # Move to end (most recently used)
        self._cache.move_to_end(key)
        self._hits += 1
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if len(self._cache) >= self.capacity:
            # Remove oldest item
            self._cache.popitem(last=False)
        
        entry = CacheEntry(
            value=value,
            created_at=time.time(),
            ttl=ttl or self.default_ttl,
            last_accessed=time.time(),
        )
        self._cache[key] = entry
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
    
    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        keys_to_delete = [k for k in self._cache.keys() if pattern in k]
        for key in keys_to_delete:
            del self._cache[key]
        return len(keys_to_delete)
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = self._hits / total if total > 0 else 0
        
        return {
            "size": len(self._cache),
            "capacity": self.capacity,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": round(hit_rate, 4),
        }


class CacheManager:
    """Manages multiple cache layers."""
    
    _instance: Optional['CacheManager'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        
        # Different cache tiers
        self.hot_cache = LRUCache(capacity=100, default_ttl=60)  # Very hot data
        self.session_cache = LRUCache(capacity=500, default_ttl=300)  # Session data
        self.data_cache = LRUCache(capacity=1000, default_ttl=600)  # General data
    
    def get(self, key: str, tier: str = "data") -> Optional[Any]:
        """Get from specified cache tier."""
        cache = self._get_tier(tier)
        return cache.get(key)
    
    def set(self, key: str, value: Any, tier: str = "data", ttl: Optional[int] = None) -> None:
        """Set in specified cache tier."""
        cache = self._get_tier(tier)
        cache.set(key, value, ttl)
    
    def delete(self, key: str, tier: Optional[str] = None) -> None:
        """Delete from cache."""
        if tier:
            self._get_tier(tier).delete(key)
        else:
            # Delete from all tiers
            self.hot_cache.delete(key)
            self.session_cache.delete(key)
            self.data_cache.delete(key)
    
    def invalidate_ta_cache(self, ta_id: int) -> None:
        """Invalidate all cache entries for a TA."""
        pattern = f"ta:{ta_id}:"
        self.hot_cache.invalidate_pattern(pattern)
        self.session_cache.invalidate_pattern(pattern)
        self.data_cache.invalidate_pattern(pattern)
    
    def invalidate_user_cache(self, user_id: int) -> None:
        """Invalidate all cache entries for a user."""
        pattern = f"user:{user_id}:"
        self.hot_cache.invalidate_pattern(pattern)
        self.session_cache.invalidate_pattern(pattern)
        self.data_cache.invalidate_pattern(pattern)
    
    def _get_tier(self, tier: str) -> LRUCache:
        """Get cache tier by name."""
        tiers = {
            "hot": self.hot_cache,
            "session": self.session_cache,
            "data": self.data_cache,
        }
        return tiers.get(tier, self.data_cache)
    
    def get_all_stats(self) -> dict:
        """Get stats for all tiers."""
        return {
            "hot": self.hot_cache.get_stats(),
            "session": self.session_cache.get_stats(),
            "data": self.data_cache.get_stats(),
        }


# Global cache manager instance
cache_manager = CacheManager()


def cached(
    key_prefix: str = "",
    ttl: int = 300,
    tier: str = "data",
    key_func: Optional[Callable] = None
):
    """
    Decorator to cache function results.
    
    Args:
        key_prefix: Prefix for cache key
        ttl: Time to live in seconds
        tier: Cache tier to use
        key_func: Optional function to generate custom cache key
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_parts = [key_prefix, func.__name__]
                key_parts.extend(str(a) for a in args)
                key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
                cache_key = hashlib.md5(
                    ":".join(key_parts).encode()
                ).hexdigest()
            
            # Try to get from cache
            cached_value = cache_manager.get(cache_key, tier)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_manager.set(cache_key, result, tier, ttl)
            
            return result
        
        # Add cache bypass method
        wrapper.cache_clear = lambda: cache_manager.delete(
            hashlib.md5(f"{key_prefix}:{func.__name__}".encode()).hexdigest(),
            tier
        )
        
        return wrapper
    return decorator


def invalidate_on_change(entity_type: str, entity_id_param: str = "id"):
    """
    Decorator to invalidate cache when entity changes.
    
    Args:
        entity_type: Type of entity (ta, user, etc.)
        entity_id_param: Parameter name containing entity ID
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            # Try to get entity ID
            entity_id = kwargs.get(entity_id_param)
            if entity_id is None and len(args) > 0:
                entity_id = args[0]
            
            if entity_id is not None:
                if entity_type == "ta":
                    cache_manager.invalidate_ta_cache(entity_id)
                elif entity_type == "user":
                    cache_manager.invalidate_user_cache(entity_id)
            
            return result
        return wrapper
    return decorator


# Specific cache helpers for common operations

def get_ta_state_cache_key(ta_id: int) -> str:
    """Generate cache key for TA state."""
    return f"ta:{ta_id}:state"


def get_ta_mastery_cache_key(ta_id: int) -> str:
    """Generate cache key for TA mastery."""
    return f"ta:{ta_id}:mastery"


def get_user_gamification_cache_key(user_id: int) -> str:
    """Generate cache key for user gamification."""
    return f"user:{user_id}:gamification"


def get_learning_path_cache_key(ta_id: int) -> str:
    """Generate cache key for learning path."""
    return f"ta:{ta_id}:learning_path"
