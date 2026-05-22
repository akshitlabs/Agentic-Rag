import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.core.redis_client import redis_client

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # User ka IP address nikalna
        client_ip = request.client.host
        current_time = time.time()
        
        # Rules: 1 minute (60 seconds) me maximum 5 requests allow karni hain
        window_time = 60 
        max_requests = 5 
        
        redis_key = f"rate_limit:{client_ip}"

        try:
            # Manager (Redis) se jaldi-jaldi 4 kaam ek saath karwa rahe hain (Pipeline)
            async with redis_client.pipeline(transaction=True) as pipe:
                # 1. 1 minute se purani entries kachre me daal do
                pipe.zremrangebyscore(redis_key, 0, current_time - window_time)
                # 2. Bachi hui (nayee) entries gino
                pipe.zcard(redis_key)
                # 3. Abhi wali nayi entry list me daal do
                pipe.zadd(redis_key, {str(current_time): current_time})
                # 4. Memory bachane ke liye 1 minute baad is list ko delete kar dena
                pipe.expire(redis_key, window_time)
                
                results = await pipe.execute()
                
            request_count = results[1] # Ye 'zcard' (ginti) ka result hai
            
            # Agar 5 se zyada bar aa gaya, toh block kar do! 🛑
            if request_count >= max_requests:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Bohot zyada requests! 🛑 Spam allowed nahi hai, thodi der baad aaiye."}
                )
                
        except Exception as e:
            # Agar kabhi Redis (Tijori/Table) band ho, toh API crash na ho, chalne do
            print(f"⚠️ Redis Error: {e}")

        # Agar limit cross nahi hui, toh aage API ke worker ke paas jaane do
        return await call_next(request)