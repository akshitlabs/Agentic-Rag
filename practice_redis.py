import asyncio
from app.core.redis_client import redis_client

async def test_redis():
    print("--- Manager ki Table (Redis) Test ---")

    # 1. Table par data rakhna (SET command)
    print("\n[+] Table par ek user session save kar rahe hain...")
    await redis_client.set("user_session_014", "Akshit_Pro_Plan") 
    print("✅ Session save ho gaya!")

    # 2. Table se data uthana (GET command)
    print("\n[+] Table se wahi session wapas maang rahe hain...")
    saved_data = await redis_client.get("user_session_014")
    print(f"🔄 Wapas mila: {saved_data}")

    # 3. Cache Expiry Test (Kachra khud saaf karna)
    print("\n[+] Ab ek naya data sirf 2 second (ex=2) ke liye rakh rahe hain...")
    # 'ex=2' ka matlab hai 2 second baad ye data khud delete ho jayega
    await redis_client.set("temp_message", "Ye file jaldi gayab ho jayegi!", ex=2)
    
    print("Turant check kiya:", await redis_client.get("temp_message"))
    
    print("⏳ 3 second wait kar rahe hain...")
    await asyncio.sleep(3) # Python ko 3 second ke liye sulate hain
    
    gayab_data = await redis_client.get("temp_message")
    print(f"3 second baad check kiya: {gayab_data}")
    
    if gayab_data is None:
        print("🎉 Magic! Data automatic table se saaf ho gaya!")

if __name__ == "__main__":
    asyncio.run(test_redis())