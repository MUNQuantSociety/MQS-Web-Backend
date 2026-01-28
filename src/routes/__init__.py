from fastapi import APIRouter

from src.routes import backtests, events, health, ibkr, leaderboard, user

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(events.router, prefix="/events", tags=["events"])
api_router.include_router(ibkr.router, prefix="/ibkr", tags=["ibkr"])
api_router.include_router(leaderboard.router, prefix="/leaderboard", tags=["leaderboard"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
api_router.include_router(user.router, prefix="/users", tags=["users"])
