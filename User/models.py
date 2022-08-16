import datetime
from database import Base
from sqlalchemy import Integer, String, Column, Text, DateTime, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    phone_number = Column(String(10), nullable=False,unique=True)
    password = Column(Text(), nullable=False)

    orders = relationship("Order", back_populates="user")
