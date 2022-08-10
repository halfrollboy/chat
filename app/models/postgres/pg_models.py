from sqlalchemy import (
    ARRAY,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Enum,
    DateTime,
    Date,
    text,
    ForeignKeyConstraint,
)
import enum
from sqlalchemy.sql import func
import datetime
from db.postgres.database import Model
from sqlalchemy.orm import relationship
from uuid import UUID, uuid4
from enum import Enum


class User(Model):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    middlename = Column(String)
    gender = Column(Enum("male", "female", "other", name="GENDER_TYPE"), nullable=False)
    birthday = Column(Date, nullable=False)
    photo_uri = Column(String, nullable=False)
    join_date = Column(Date, nullable=False, server_default=text("now()"))
    is_online = Column(Boolean, nullable=False, server_default=text("false"))
    last_seen = Column(DateTime, nullable=False, server_default=text("now()"))


class UserSetting(User):
    __tablename__ = "user_settings"

    id = Column(ForeignKey("users.id"), primary_key=True)
    allow_avatar_suggestions = Column(Boolean, server_default=text("false"))
    allow_sync_calendar = Column(Boolean, server_default=text("false"))
    allow_profile_sharing = Column(Boolean, server_default=text("false"))


class Message(Model):
    __tablename__ = "messages"
    __table_args__ = (
        ForeignKeyConstraint(
            ["chat_id", "reply_to"], ["messages.chat_id", "messages.message_id"]
        ),
    )

    chat_id = Column(ForeignKey("chats.id"), primary_key=True, nullable=False)
    message_id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        server_default=text("nextval('messages_message_id_seq'::regclass)"),
    )
    user_id = Column(ForeignKey("users.id"), nullable=False)
    reply_to = Column(Integer)
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))
    edited_at = Column(DateTime)
    content = Column(String)
    attachments = Column(ARRAY(Integer()))
    is_pinned = Column(Boolean, server_default=text("false"))

    chat = relationship("Message", remote_side=[chat_id, message_id])
    chat1 = relationship("Chat")
    user = relationship("User")


class Attachment(Model):
    __tablename__ = "attachments"

    id = Column(UUID, primary_key=True)
    type = Column(
        Enum(
            "link",
            "image",
            "document",
            "other",
            "message",
            "note",
            "event",
            "news",
            name="ATTACHMENT_TYPE",
        ),
        nullable=False,
    )
    created_at = Column(DateTime)
    edited_at = Column(DateTime)
    uri = Column(String, nullable=False)
    default_permissions = Column(
        String(4), server_default=text("'r-s-'::character varying")
    )

    workspaces = relationship("Workspace", secondary="workspace_attachment")


class AttachmentUser(Model):
    __tablename__ = "attachment_user"

    attachment_id = Column(
        ForeignKey("attachments.id"), primary_key=True, nullable=False
    )
    user_id = Column(ForeignKey("users.id"), primary_key=True, nullable=False)
    permissions = Column(String(4))

    attachment = relationship("Attachment")
    user = relationship("User")


class Chat(Model):
    __tablename__ = "chats"

    id = Column(UUID, primary_key=True)
    type = Column(
        Enum("global", "avatar", "personal", "group", name="CHAT_TYPE"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, server_default=text("now()"))


class ChatType(Enum):
    """Для использования вне таблиц"""

    GLOBAL = "global"
    AVATAR = "avatar"
    PERSONAL = "personal"
    GROUP = "group"


class ChatUser(Model):
    __tablename__ = "chat_user"

    chat_id = Column(ForeignKey("chats.id"), primary_key=True, nullable=False)
    user_id = Column(ForeignKey("users.id"), primary_key=True, nullable=False)
    permissions = Column(String(8))
    last_read_id = Column(Integer, server_default=text("'-1'::integer"))
    is_muted = Column(Boolean, server_default=text("false"))
    mute_end = Column(Date)
    is_left = Column(Boolean, server_default=text("false"))

    chat = relationship("Chat")
    user = relationship("User")


class PersonalChat(Model):
    __tablename__ = "personal_chats"

    id = Column(UUID, primary_key=True)
    chat_id = Column(ForeignKey("chats.id"))

    chat = relationship("Chat")


class GroupChat(Model):
    __tablename__ = "group_chats"
    id = (Column("id", ForeignKey("chats.id")),)
    name = (Column("name", String, nullable=False, unique=True),)
    title = (Column("title", String),)
    description = (Column("description", String),)
    photo_uri = (
        Column(
            "photo_uri",
            String,
            server_default=text("'random generated'::character varying"),
        ),
    )
    default_permissions = (
        Column(
            "default_permissions",
            String(8),
            server_default=text("'rwspi---'::character varying"),
        ),
    )
    owner_id = Column("owner_id", ForeignKey("users.id"))
