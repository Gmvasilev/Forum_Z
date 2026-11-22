from fastapi import FastAPI
import uvicorn


# TODO: import routers and include them, remove todo comments after

from routers.api.replies_api_router import replies_api_router
from routers.api.topics_api_router import topics_api_router
from routers.api.users_api_router import users_api_router
from routers.api.auth_api_router import auth_api_router
# todo: import reactions_api_router

from routers.web.home_router import home_router
from routers.web.topics_router import topics_routers
# todo: import  replies_router
# todo: import reactions_router
# todo: import users_router


RELOAD_SERVER = True # True reloads the server after every saved modification


app = FastAPI(title="Forum Z")


# *** API Routers ***
app.include_router(replies_api_router)
app.include_router(topics_api_router)
app.include_router(users_api_router)
app.include_router(auth_api_router)
# todo: reactions_api_router

# *** WEB Routers ***
app.include_router(home_router)
app.include_router(topics_routers)
# todo: other web routers


# *** Run Server ***
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=RELOAD_SERVER)

