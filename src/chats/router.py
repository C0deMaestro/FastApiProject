from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.models.models import Chat,Message, User


router = APIRouter(
    prefix="/chats",
    tags=["Chat"]
)

@router.get("/find_chats")
async def find_chats(chat_name:str, session: AsyncSession = Depends(get_async_session)):
    query = select(Chat).where(Chat.chat_name == chat_name)
    result = await session.execute(query)
    return result.scalars().all()

@router.get("/find_users")
async def find_users(user_name:str, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.username == user_name)
    result = await session.execute(query)
    return result.scalars().all()