""

from app.auth.schemas.jwt import RefreshTokenSchema, TokensSchema
from app.auth.schemas.auth import LoginSchema
from app.auth.services.jwt import JwtService
from app.auth.services.utils import verify_password
from app.auth.exceptions.auth import BadCredentialsException
from app.user.services.user import UserService
from core.helpers.hashids import encode


class AuthService:
    """
    Service class for handling authentication-related functionality.

    Attributes:
        jwt (JwtService): An instance of the JwtService class for handling JSON Web 
        Tokens.
        user_serv (UserService): An instance of the UserService class for interacting 
        with user 
        data.

    Methods:
        login(username: str, password: str) -> TokensSchema:
            Authenticates a user by their display name and password, and returns a pair 
            of JSON Web Tokens.
    """

    def __init__(self, session) -> None:
        """
        Initializes an instance of the AuthService class.
        """
        self.user_serv = UserService(session)
        self.jwt_serv = JwtService()

    async def login(self, schema: LoginSchema) -> TokensSchema:
        """
        Authenticates a user by their display name and password, and returns a pair of 
        JSON Web Tokens.

        Args:
            username (str): The user's display name.
            password (str): The user's password.

        Raises:
            UserNotFoundException: If a user with the provided display name is not 
            found.
            IncorrectPasswordException: If the provided password does not match the 
            user's password.

        Returns:
            TokensSchema: A pair of JSON Web Tokens (access and refresh tokens).
        """
        user = await self.user_serv.get_by_username(schema.username)
        if not user:
            raise BadCredentialsException()
        if not verify_password(schema.password, user.password):
            raise BadCredentialsException()
        
        user_id = encode(user.id)

        return self.jwt_serv.create_login_tokens(user_id=user_id)
    
    async def refresh(self, schema: RefreshTokenSchema):
        """Generate a new token pair depending on the refresh token.
        
        Args:
            refresh_token (str): The refresh JWT.
            
        Returns:
            TokenSchema
        """
        return JwtService().refresh_tokens(refresh_token=schema.refresh_token)