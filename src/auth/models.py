from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, MetaData
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database import Base

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from datetime import datetime




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

    #Созданные чаты
    chats_admin= relationship("Chat",backref="admin")

    #в каких чатах состоишь
    chats = relationship("Chat", secondary="user_chat_relations", back_populates="users")








