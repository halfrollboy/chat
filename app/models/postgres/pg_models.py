from email.policy import default
from faulthandler import disable
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Enum
import enum
from ...db.postgres.database import Model
from uuid import UUID


class Chat_type(enum.Enum):
    # global = 1
    avatar = 2
    personal = 3
    grpup = 4

class Chats(Model):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200))
    type = Column()


class User(Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(200), unique=True)
    fullname = Column(String(200))
    password = Column(String(200))
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True)
    # disabled = Column(Boolean)


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
