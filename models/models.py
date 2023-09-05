from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class UserChatRelations(Base):
    __tablename__ = "user_chat_relations"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), primary_key=True)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    telephone = Column(Integer, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    register_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Определение связей между моделями User и Chat
    chats = relationship("Chat", secondary="user_chat_relations", back_populates="users")


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)
    chat_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    user_created_id = Column(Integer, ForeignKey("users.id"))
    register_at = Column(TIMESTAMP, default=datetime.utcnow)

    # Определение связей между моделями Chat и User
    users = relationship("User", secondary="user_chat_relations", back_populates="chats")


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    user_created_id = Column(Integer, ForeignKey("users.id"))
    time_send = Column(TIMESTAMP, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)

