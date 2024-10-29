from fastapi import APIRouter

menzhenAPI = APIRouter(prefix="/menzhen",tags=["门诊"])

@menzhenAPI.get("/")
async def index():
    return {"message": "门诊"}

