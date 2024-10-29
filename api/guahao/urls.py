from fastapi import APIRouter
from db.database import *


guahaoAPI = APIRouter(prefix="/guahao",tags=["挂号"])

@guahaoAPI.get("/")
async def index():

    conn = get_connection()

    return {
        "status": "success",
        "message": "Welcome to the Guahao API!",
        "data": [
            {
                "id": 1,
                "name": "Dr. Smith",
                "specialty": "Cardiology",
                "location": "New York",
                "available": True,
                "price": 200
            },
            {
                "id": 2,
                "name": "Dr. Johnson",
                "specialty": "Neurology",
                "location": "Los Angeles",
                "available": False,
                "price": 250
            }
        ]
    }


