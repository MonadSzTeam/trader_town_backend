from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, DECIMAL, UniqueConstraint
from sqlalchemy.sql import func
from datetime import datetime
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    balance: Mapped[float] = mapped_column(DECIMAL(20, 8), default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    orders: Mapped[List["Order"]] = relationship(back_populates="user")
    portfolio_items: Mapped[List["Portfolio"]] = relationship(back_populates="user")

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    current_price: Mapped[float] = mapped_column(DECIMAL(20, 8), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    orders: Mapped[List["Order"]] = relationship(back_populates="item")
    portfolio_entries: Mapped[List["Portfolio"]] = relationship(back_populates="item")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    order_type: Mapped[str] = mapped_column(String(10), nullable=False) # 'BUY' or 'SELL'
    price: Mapped[float] = mapped_column(DECIMAL(20, 8), nullable=False)
    quantity: Mapped[float] = mapped_column(DECIMAL(20, 8), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="PENDING") # 'PENDING', 'COMPLETED', 'CANCELLED'
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="orders")
    item: Mapped["Item"] = relationship(back_populates="orders")

class Portfolio(Base):
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(DECIMAL(20, 8), default=0.0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship(back_populates="portfolio_items")
    item: Mapped["Item"] = relationship(back_populates="portfolio_entries")

    __table_args__ = (UniqueConstraint('user_id', 'item_id', name='unique_user_item'),)
