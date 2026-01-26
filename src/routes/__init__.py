from fastapi import APIRouter

from src.routes import (
    auth,
    billing,
    billing_webhook,
    chats,
    health,
    plans,
    uploads,
    usage,
    user,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
api_router.include_router(billing_webhook.router, prefix="/billing", tags=["billing"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(usage.router, prefix="/usage", tags=["usage"])
api_router.include_router(chats.router, prefix="/chats", tags=["chats"])
api_router.include_router(plans.router, prefix="/plans", tags=["plans"])
api_router.include_router(health.router, tags=["health"])
