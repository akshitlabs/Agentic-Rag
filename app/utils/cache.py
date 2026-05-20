import json
from functools import wraps
from app.core.redis_client import redis_client

# Ye hamara smart assistant (Decorator) hai
def cache_response(expire_seconds=60): # By default 60 second tak yaad rakhega
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 1. Sawal ke hisaab se ek unique naam (Key) banana
            # (Taki har alag sawal ka alag answer save ho)
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # 2. Check karna ki kya answer pehle se table (Redis) par hai?
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                print("⚡ FAST ANSWER (Cache Hit): Manager ki table se turant mil gaya!")
                # JSON string ko wapas Python dictionary/data me badalna
                return json.loads(cached_data)
            
            # 3. Agar table par nahi mila, toh asli function chalao (Hard Work)
            print("🐢 SLOW WORK (Cache Miss): Asli Godown/AI se mangwa rahe hain...")
            result = await func(*args, **kwargs)
            
            # 4. Asli answer milne ke baad, usko aage ke liye table par save kar lo!
            await redis_client.set(cache_key, json.dumps(result), ex=expire_seconds)
            
            return result
        return wrapper
    return decorator