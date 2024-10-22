from fastapi import APIRouter
from routers import accounts, offers

api_router = APIRouter()
api_router.include_router(offers.router)
api_router.include_router(accounts.router)
