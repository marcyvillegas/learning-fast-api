from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100))
    password = Column(String(100))

    posts = relationship("Post", back_populates="user")

