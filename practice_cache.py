import asyncio
import time
from app.utils.cache import cache_response

# Ye function jaan-bujh kar 5 second lagata hai (Heavy Task)
# Humne iske upar apna Cache Decorator laga diya hai!
@cache_response(expire_seconds=60)
async def slow_function(sawal: str):
    print(f"[{sawal}] ka answer dhoondhne me time lag raha hai...")
    await asyncio.sleep(5) # 5 second ka wait
    return {"sawal": sawal, "answer": "Ye raha aapka lamba-chauda answer!"}

async def test_decorator():
    print("--- Cache Decorator Live Test ---\n")
    
    # 1. Pehli baar sawal pucha (Isme 5 second lagne chahiye)
    print("👉 TEST 1: Pehli Baar (User 1 ne sawal pucha)")
    start_time = time.time()
    result1 = await slow_function("Agentic RAG kya hai?")
    print(f"⏳ Nateeja mila. Time laga: {time.time() - start_time:.2f} seconds\n")

    # 2. Dusri baar wahi sawal pucha (Ye turant hona chahiye)
    print("👉 TEST 2: Dusri Baar (User 2 ne wahi same sawal pucha)")
    start_time2 = time.time()
    result2 = await slow_function("Agentic RAG kya hai?")
    print(f"⚡ Nateeja mila. Time laga: {time.time() - start_time2:.2f} seconds\n")

    # 3. Ek naya sawal pucha (Isme wapas 5 second lagne chahiye)
    print("👉 TEST 3: Teesra Baar (User 3 ne ek naya sawal pucha)")
    start_time3 = time.time()
    result3 = await slow_function("Python kab bani thi?")
    print(f"⏳ Nateeja mila. Time laga: {time.time() - start_time3:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(test_decorator())