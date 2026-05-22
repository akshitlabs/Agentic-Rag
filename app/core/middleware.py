import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Jaise hi koi API call aati hai, stopwatch chalu kar do
        start_time = time.time()
        print(f"📹 [CCTV] Nayi request aayi: {request.method} {request.url.path}")
        
        # 2. Request ko API ke andar jaane do aur answer (response) aane ka wait karo
        response = await call_next(request)
        
        # 3. Answer aane ke baad stopwatch band karo aur time check karo
        process_time = time.time() - start_time
        print(f"✅ [CCTV] Request puri hui: Status {response.status_code} | Time: {process_time:.4f} seconds\n")
        
        return response