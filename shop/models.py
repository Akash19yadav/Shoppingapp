from sqlalchemy import Column, String, DECIMAL, Integer, TEXT, DateTime, ForeignKey, Boolean
from sqlalchemy_utils import URLType
from database import Base
from sqlalchemy.orm import relationship
import datetime


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    slug = Column(String(20), unique=True)

    product_category = relationship("Product", back_populates="category_related")


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(TEXT)
    url = Column(URLType)
    available = Column(Boolean, default=True)
    price = Column(DECIMAL(scale=2), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.datetime.utcnow)
    slug = Column(String(20), unique=True)

    category_id = Column(Integer, ForeignKey("category.id"))
    category_related = relationship("Category", back_populates="product_category")

    product_order = relationship("OrderItem", back_populates="product_related")
