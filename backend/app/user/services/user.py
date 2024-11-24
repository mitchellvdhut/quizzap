from app.user.schemas.user import CreateUserSchema, UpdateUserSchema
from app.auth.services.utils import get_password_hash
from app.user.exceptions.user import DuplicateUsernameException, UserNotFoundException
from app.user.repository.user import UserRepository
from core.db.models import User


class UserService:
    def __init__(self, session) -> None:
        self.repo = UserRepository(session)

    async def get_by_username(self, username):
        return self.repo.get_by_username(username)

    async def create_user(self, schema: CreateUserSchema):
        user = self.repo.get_by_username(schema.username)

        if user:
            raise DuplicateUsernameException

        hashed_pass = get_password_hash(schema.password)
        user = User(username=schema.username, password=hashed_pass)
        return self.repo.create(user)

    async def delete_user(self, user_id: int) -> None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        
        self.repo.delete(user)

    async def update_user(self, user_id: int, schema: UpdateUserSchema):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        
        hashed_pass = get_password_hash(schema.password)
        params = {"username": schema.username, "password": hashed_pass}
        
        self.repo.update_by_id(user_id, params)
        return self.repo.get_by_id(user_id)
    
    async def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        
        return user
    
    async def get_users(self):
        return self.repo.get()
    
    async def is_admin(self, user_id):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException
        
        return user.is_admin

