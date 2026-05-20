import redis.asyncio as redis
from app.core.config import settings

# Manager ki Table (Redis) ka connection setup
redis_client = redis.from_url(
    settings.redis_url, 
    encoding="utf-8", 
    decode_responses=True # Ye bohot zaroori hai! Isse data ajeeb format (bytes) me nahi, balki aasan text (strings) me milta hai.
)