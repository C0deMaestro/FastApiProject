from typing import List

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, WebSocket, Request, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.messages.shemas import MessageModel
from src.models.models import Message

templates = Jinja2Templates(directory="src/templates")

router = APIRouter(
    prefix="/messages",
    tags=["message"]
)
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            data = await websocket.receive_text()
            # Send message to the client
            await manager.send_personal_message(f"Message text was: {data}",websocket)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')


@router.get("/send")
def get_chat_page(request: Request):
    print("111111111111111111111",templates)
    return templates.TemplateResponse("chat.html", {"request": request})

@router.get("/last_messages")
async def get_last_messages(
        session: AsyncSession = Depends(get_async_session),) -> List[MessageModel]:
    query = select(Message).order_by(Message.id.desc()).limit(5)
    messages = await session.execute(query)
    return messages.scalars().all()