from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.models.reply import ReplyCreate, ReplyResponse, ReplyUpdate
from app.routers.dependencies import get_current_user
from app.services import replies_service

replies_api_router = APIRouter(prefix="/api", tags=["Replies"])


