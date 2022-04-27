from fastapi import APIRouter

from app.api.routes import main_page

login_api_router = APIRouter()
login_api_router.include_router(main_page.router, tags=['posts'])
