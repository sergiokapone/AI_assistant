### Import from FastAPI ###

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
    status,
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordRequestForm,
)
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.db_helper import db_helper
from ..repository import users as repository_users
from ..schemas.auth import TokenSchema
from ..schemas.users import UserSchema
from ..services.auth import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


@router.post(
    "/signup",
    name="signup",
    description="Root is designed for user registration",
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    body: UserSchema,
    # request: Request,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    exist_user_email = await repository_users.get_user_by_email(body.email, session)
    exist_user_username = await repository_users.get_user_by_username(
        body.username, session
    )

    if exist_user_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    if exist_user_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )

    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, session)

    return {"user": new_user, "detail": "SUCCESS_CREATE_USER"}


@router.post("/login", response_model=TokenSchema)
async def login(
    # response:Response,
    body: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    
    user = await repository_users.get_user_by_email(body.username, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_EMAIL"
        )

    # Check is_active

    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_PASSWORD"
        )

    # Generate JWT
    access_token = await auth_service.create_access_token(
        data={"email": user.email}, expires_delta="TOKEN_LIFE_TIME"
    )

    tokens = TokenSchema(access_token=access_token)

    return tokens


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Security(security),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    # current_user: User = Depends(auth_service.get_authenticated_user),
):
    """
    **Log out user and add the token to the blacklist.**

    This route allows the user to log out and their access token will be added to the blacklist.

    Level of Access:

    - Current authorized user

    :param credentials: HTTPAuthorizationCredentials: User authentication data (token).

    :param db: AsyncSession: Database Session.

    :param current_user: User: Current authenticated user.

    :return: A message informing you that the user has successfully logged out of the system.

    :rtype: MessageResponseSchema
    """

    token = credentials.credentials

    await repository_users.add_to_blacklist(token, session)
    return {"message": "USER_IS_LOGOUT"}
