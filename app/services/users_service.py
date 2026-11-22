from models.user_models import UserIn, UserOut
from repositories import users_repository





def create(user: UserIn) -> UserOut:
    
    user_id = users_repository.insert(user.model_dump())
    
    return UserOut(
        user_id=user_id,
        username= user.username,
        rating=0
        )
    
    