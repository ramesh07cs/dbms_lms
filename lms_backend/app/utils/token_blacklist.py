# app/utils/token_blacklist.py

import os
import time
try:
    import redis
except Exception:
    redis = None

# Environment variable to configure Redis (optional)
REDIS_URL = os.getenv("REDIS_URL")
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "token_blacklist:")

# Fallback in-memory set if Redis is not available/configured
_IN_MEMORY_BLACKLIST = set()


def _get_redis_client():
    if not REDIS_URL or redis is None:
        return None
    try:
        return redis.from_url(REDIS_URL)
    except Exception:
        return None


def add_token_to_blacklist(jti, expires=None):
    """
    Add a token `jti` to blacklist. If Redis is configured, store with optional TTL (seconds).
    Otherwise use in-memory set. `expires` is optional seconds to expire the blacklist entry.
    """
    client = _get_redis_client()
    if client:
        key = REDIS_PREFIX + str(jti)
        try:
            if expires:
                client.setex(key, int(expires), "1")
            else:
                client.set(key, "1")
        except Exception:
            # fallback to in-memory on error
            _IN_MEMORY_BLACKLIST.add(jti)
    else:
        _IN_MEMORY_BLACKLIST.add(jti)


def is_token_blacklisted(jti):
    """
    Return True if token `jti` is blacklisted.
    Checks Redis first (if configured), otherwise in-memory set.
    """
    client = _get_redis_client()
    if client:
        try:
            key = REDIS_PREFIX + str(jti)
            return client.exists(key) == 1
        except Exception:
            return jti in _IN_MEMORY_BLACKLIST
    return jti in _IN_MEMORY_BLACKLIST


def clear_blacklist():
    """Clear in-memory blacklist (for tests). Does not affect Redis."""
    _IN_MEMORY_BLACKLIST.clear()
