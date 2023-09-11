from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import auth_backend, fastapi_users
#from src.chats.models import Chat
from src.auth.schemas import UserRead, UserCreate
from src.chats.router import router as chats_router

app = FastAPI(
    title="Message_App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(chats_router)
