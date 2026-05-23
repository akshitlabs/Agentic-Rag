import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Ye decorator batata hai ki hamara test async (fast) hai
@pytest.mark.asyncio
async def test_health_check():
    # Hamari API ko ek nakli request bhej rahe hain
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    
    # Check kar rahe hain ki API ne 200 OK aur sahi message diya ya nahi
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy", 
        "message": "API is running!" 
    }