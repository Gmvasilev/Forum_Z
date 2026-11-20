
from fastapi import(
    APIRouter,
    Request
)








users_router = APIRouter(prefix="/users")






# --- GET User Registration Form ---
@users_router.get("/new", response_model=)
def get_register_form(request: Request):
    return 


# --- POST User Registration Form
@users_api_router.post("")
def submit_register_form(