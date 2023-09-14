from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_user
from src.chats.schemas import ChatCreate
from src.database import get_async_session
from src.models.models import Chat, User, UserChatRelations

router = APIRouter(
    prefix="/chats",
    tags=["chat"]
)


@router.get("/view_all_chats")
async def view_all_chats(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Chat)
        result = await session.execute(query)
        return {
                    "status": "success",
                    "data": result.scalars().all(),
                    "details": None
                }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.get("/find_chats")
async def find_chats(chat_name:str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Chat).where(Chat.chat_name == chat_name)
        print("11111111111",query)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": query,
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })

@router.post("/create_chat")
async def create_chat(
        chat_created: ChatCreate,
        user : User = Depends(current_user),# Список ID пользователей, которых пользователь хочет добавить в чат
        session: AsyncSession = Depends(get_async_session)
    ):

    # Проверяем, существует ли пользователь с указанным ID
    user = await session.get(User,  user.id)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    # Создаем новый чат
    new_chat = Chat(chat_name=chat_created.chat_name, user_created=user)

    session.add(new_chat)
    await session.commit()

    # Создаем связь между пользователем и чатом в таблице user_chat_relations
    user_chat_relation = UserChatRelations(user_id=user.id, chat_id=new_chat.id)
    session.add(user_chat_relation)

    # Добавляем выбранных пользователей в чат
    for member_id in chat_created.users:
        member = await session.get(User, member_id)
        if member is not None:
            user_chat_relation = UserChatRelations(user_id=member_id, chat_id=new_chat.id)
            session.add(user_chat_relation)

    await session.commit()
    return {"message": "Чат успешно создан", "chat_id": new_chat.id}



@router.get("/find_users")
async def find_users(user_name:str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.username == user_name)
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.scalars().all(),
            "details": None
        }
    except:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })
