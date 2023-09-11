from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base



class Chat(Base):
    __tablename__ = "chat"
    id = Column(Integer, primary_key=True)
    chat_name = Column(String, nullable=False)
    username = Column(String, nullable=False)
    register_at = Column(TIMESTAMP, default=datetime.utcnow)

    #создатель чата
    user_created_id = Column(Integer, ForeignKey("user.id"))
    user_created = relationship("User",backref="chats_creator")

    #пользователи чата
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