from email.policy import default
from faulthandler import disable
from typing import List
from h11 import Data
from sqlalchemy import (
    ARRAY,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Enum,
    DateTime,
)
from sqlalchemy.ext.mutable import MutableList
import enum
from sqlalchemy.sql import func
import datetime
from ...db.postgres.database import Model
from uuid import UUID, uuid4
from ...models.pydantic.chat import ChatType
from ...models.pydantic.user import GenderType


class Messages(Model):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    chat_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    reply_to = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    edited_at = Column(DateTime(timezone=True), onupdate=func.now())
    content = Column(String)
    attachment = Column(MutableList.as_mutable(ARRAY(UUID)), unique=False)


class Chats(Model):
    __tablename__ = "chats"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(200))
    type = Column(ChatType)
    title = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    discription = Column(String)
    photo_uri = Column(String)
    default_permissions = Column(String(200))
    owner_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(200), unique=True)
    firstname = Column(String(200))
    lastname = Column(String(200))
    middlname = Column(String(200))
    gender = Column(GenderType)
    birthday = Column(DateTime)
    photo_uri = Column(String)
    join_date = Column(DateTime)
    is_online = Column(Boolean)
    last_seen = Column(DateTime)  # Точно ли

    # Пока оставлю так чтобы была какая-то регистрация
    password = Column(String(200))
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)


class Company(Model):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String, unique=True)
    email = Column(String, unique=True, index=True)
    adress = Column(String)
    coordinate = Column(String)
    info_id = Column(Integer)
    edited = Column(Boolean, nullable=False, default=True)


class Employee(Model):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    fio = Column(String(200))
    phone = Column(String, unique=True)
    company_id = Column(Integer, ForeignKey("company.id"))
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    gender = Column(Boolean, nullable=False)
    info = Column(Integer)
    admin = Column(Boolean, nullable=False)
    owner = Column(Boolean, nullable=False)
