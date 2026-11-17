# TODO: API router for users

from fastapi import APIRouter


users_api_router = APIRouter(prefix = '/users', tags=["Users"])
