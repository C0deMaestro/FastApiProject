from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, MetaData
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from datetime import datetime

metadata = Base.metadata


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    telephone = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


    chats = relationship("Chat", secondary="user_chat_relations", back_populates="users")


class Chat(Base):
    __tablename__ = "chat"
    __tableargs__ ={"metadata":metadata}
    id = Column(Integer, primary_key=True)
    chat_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    register_at = Column(TIMESTAMP, default=datetime.utcnow)

    #создатель чата
    user_created_id = Column(Integer, ForeignKey("user.id"))
    user_created = relationship("User",backref="chats_admin")

    users = relationship("User", secondary="user_chat_relations", back_populates="chats")


class UserChatRelations(Base):
    __tablename__ = "user_chat_relations"
    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    chat_id = Column(Integer, ForeignKey("chat.id"), primary_key=True)



class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_created_id = Column(Integer, ForeignKey("user.id"))
    time_send = Column(TIMESTAMP, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)




