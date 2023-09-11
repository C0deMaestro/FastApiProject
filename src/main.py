from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import auth_backend, fastapi_users
from src.chats.models import Chat
from src.auth.schemas import UserRead, UserCreate
from src.database import get_async_session

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


@app.get("/find_users")
async def find_chats(chat_name:str, session: AsyncSession = Depends(get_async_session)):
    chat = Chat
    query = select(chat).where(chat.chat_name == chat_name)
    print(query)
    result = await session.execute(query)
    print(result)
    return result.all()

