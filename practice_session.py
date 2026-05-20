import asyncio
import json
from app.core.redis_client import redis_client

async def chat_memory_test():
    print("--- AI Chatbot / Voice Assistant Memory Test ---\n")
    
    # Ek unique user ka session ID
    session_id = "chat_history:user_999"
    
    # Test shuru karne se pehle purani history saaf kar dete hain
    await redis_client.delete(session_id)

    print("📞 [User]: Hello, mujhe Callingmate ke baare me kuch puchna hai.")
    
    # 1. User ka message List me add karna (rpush)
    user_msg = {"role": "user", "content": "Hello, mujhe Callingmate ke baare me kuch puchna hai."}
    await redis_client.rpush(session_id, json.dumps(user_msg))
    
    print("🤖 [AI]: Zaroor! Boliye main aapki kya madad kar sakta hoon?")
    
    # 2. AI ka answer bhi List me add karna (rpush)
    ai_msg = {"role": "assistant", "content": "Zaroor! Boliye main aapki kya madad kar sakta hoon?"}
    await redis_client.rpush(session_id, json.dumps(ai_msg))
    
    print("\n⏳ Thodi der baad AI database se memory check kar raha hai...\n")
    
    # 3. Poori chat history wapas nikalna (0 se -1 ka matlab hai First se Last tak sab)
    history = await redis_client.lrange(session_id, 0, -1)
    
    print("🧠 AI ko ye pichli baatein yaad hain:")
    for item in history:
        msg = json.loads(item)
        print(f" -> {msg['role'].upper()}: {msg['content']}")
        
    # 4. Chat history par Expiry lagana (TTL)
    # (Taki Godown me kachra jama na ho, 1 ghante baad chat khud delete ho jayegi)
    await redis_client.expire(session_id, 3600) 
    
    print("\n✅ Session memory successfully test ho gayi!")

if __name__ == "__main__":
    asyncio.run(chat_memory_test())