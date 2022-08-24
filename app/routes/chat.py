# import asyncio
# from time import sleep
# import uvicorn
from plistlib import UID
from fastapi import FastAPI, APIRouter, Depends, Query, Path
from sse_starlette import EventSourceResponse
from repositories.chat import ChatRepository
from repositories.message import MessageRepository

# from services.chat.chat import Chat
from uuid import UUID
from pydantic import parse_obj_as
from typing import List
from models.pydantic.chat import Chat, ChatBase, ChatCreate
from datetime import datetime
from services.chat.chat import Chat as ChatService


router_chat = APIRouter(
    prefix="/chat",
    tags=["chat"],
    # dependencies=[Depends(get_token_handler)],
    responses={404: {"messages": "Not found"}},
)

chat_service = ChatService()


@router_chat.get("/", response_model=List[Chat])
async def get_list_chats(
    skip: int = 0, max: int = 10, chats: ChatRepository = Depends()
):
    db_user = await chats.all(skip=skip, max=max)
    return parse_obj_as(List[Chat], db_user)


@router_chat.post("/{chat_id}/message/{message_id}/delete")
async def delete_message_from_chat(
    chat_id: UUID = Path(...),
    message_id: int = Path(...),
    message_rep: MessageRepository = Depends(),
):
    return_msg = await message_rep.delete_message_from_chat(
        chat_id=chat_id, message_id=message_id
    )
    return return_msg


@router_chat.get("/chat/{chat_id}/info")
async def get_chat_info(chat_id: UUID = Path(...), chats: ChatRepository = Depends()):
    info = await chats.find_group_info(chat_id=chat_id)
    return info


@router_chat.post("/chat/{chat_id}/info/edit")
async def edit_chat_info(chat_id: UUID = Path(...)):
    pass


@router_chat.get("/chat/{chat_id}/messages")
async def get_chat_messages(chat_id: UUID = Path(...)):
    return await chat_service.get_messages_from_chat(chat_id=chat_id)


@router_chat.get("/chat/{chat_id}/message/{message_id}")
async def get_message(
    chat_id: UUID = Path(...),
    message_id: int = Path(...),
    messages: MessageRepository = Depends(),
):
    return await messages.get_message_with_chat(chat_id=chat_id, message_id=message_id)


@router_chat.post("/chat/{chat_id}/leave")
async def leave_chat(chat_id: UUID = Path(...), chats: ChatRepository = Depends()):
    user_id = "4ea558c3-dbbc-44f4-8a51-c58dbe962275"
    return await chats.leave_from_chat(chat_id=chat_id, user_id=user_id)


@router_chat.post("/chat/{chat_id}/join")
async def join_to_chat(chat_id: UUID = Path(...), chats: ChatRepository = Depends()):
    """Пользователь добавляется сам"""
    user_id = "4ea558c3-dbbc-44f4-8a51-c58dbe962275"
    return await chats.add_user_to_chat(chat_id=chat_id, user_id=user_id)


@router_chat.post("/chat/{chat_id}/add/user/{user_id}")
async def add_user(
    chat_id: UUID = Path(...),
    user_id: UUID = Path(...),
    chats: ChatRepository = Depends(),
):
    """Добавить пользовател в групповой чат"""
    return await chats.add_user_to_chat(chat_id=chat_id, user_id=user_id)


# TODO что возвращаем
@router_chat.post("/chat/{chat_id}/add/user/{user_id}")
async def add_user(
    chat_id: UUID = Path(...), user_id=Path(...), chats: ChatRepository = Depends()
):
    return await chats.add_user_to_chat(chat_id=chat_id, user_id=user_id)


@router_chat.post("/chat/{chat_id}/remove/user/{user_id}")
async def remove_user(chat_id: UUID, user_id: UUID, chats: ChatRepository = Depends()):
    return await chats.delete_user_from_chat(chat_id=chat_id, user_id=user_id)


@router_chat.post("/chat/{chat_id}/mute")
async def mute_chat(
    chat_id: UUID,
    time: datetime = Query(None, description="Используется для блокировки на время"),
    chats: ChatRepository = Depends(),
):
    user_id = "4ea558c3-dbbc-44f4-8a51-c58dbe962275"
    return await chats.mute_chat(chat_id=chat_id, user_id=user_id)


# TODO не нашёл в базе
@router_chat.post("/chat/{chat_id}/message/{message_id}/read")
async def read_message(
    chat_id: UUID = Path(...),
    message_id: int = Path(...),
    chats: ChatRepository = Depends(),
):
    # Записываем id последнего прочитанного сообщения
    user_id = "4ea558c3-dbbc-44f4-8a51-c58dbe962275"
    await chats.last_read_message(
        chat_id=chat_id, user_id=user_id, message_id=message_id
    )


@router_chat.get("/chat/is_chatname_available/{chatname}")
async def is_chatname_available(chatname: str, chats: ChatRepository = Depends()):
    return await chat_service.check_name_is_free(chatname)


# TODO проверить
@router_chat.post("/chat/create")
async def create_chat(create: ChatCreate, service: ChatService = Depends()):
    responce = await service.create_chat(create)
    return responce


@router_chat.get("/chat/{chat_id}/info/attachments")
async def get_attachments(
    chat_id: UUID = Path(...), messages_rep: MessageRepository = Depends()
):
    return await messages_rep.get_attachemnts_unic(chat_id=chat_id)
