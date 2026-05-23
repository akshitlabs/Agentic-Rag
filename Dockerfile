# 1. Python ka ek halka-phulka version le rahe hain
FROM python:3.12-slim

# 2. Container ke andar ek /app folder bana rahe hain
WORKDIR /app

# 3. 'uv' package manager install kar rahe hain
RUN pip install uv

# 4. Apne computer ka saara code container me copy kar rahe hain
COPY . .

# 5. API ko start karne ki aakhiri command
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]