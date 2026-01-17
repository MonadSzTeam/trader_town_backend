from sqlalchemy.orm import Session
from app.db import models
from app.db.models import User, Item, Order, Portfolio
from typing import List, Optional
from datetime import datetime

# --- User Operations ---
def create_user(db: Session, username: str, email: str, password_hash: str) -> User:
    db_user = User(username=username, email=email, password_hash=password_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

# --- Item Operations ---
def create_item(db: Session, name: str, symbol: str, current_price: float, description: str = None) -> Item:
    db_item = Item(name=name, symbol=symbol, current_price=current_price, description=description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int) -> Optional[Item]:
    return db.query(Item).filter(Item.id == item_id).first()

# --- Order Operations ---
def create_order(db: Session, user_id: int, item_id: int, order_type: str, price: float, quantity: float) -> Order:
    db_order = Order(
        user_id=user_id,
        item_id=item_id,
        order_type=order_type,
        price=price,
        quantity=quantity,
        status="PENDING"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> List[Order]:
    return db.query(Order).offset(skip).limit(limit).all()

def get_user_orders(db: Session, user_id: int) -> List[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()
