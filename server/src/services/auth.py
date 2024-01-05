from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from ..config.settings import settings
from ..database.db_helper import db_helper
from ..repository import users as repository_users


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/{settings.api_prefix}/auth/login")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: int | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(minutes=150)
        else:
            expire = datetime.utcnow() + timedelta(minutes=150)
        to_encode.update(
            {"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM
        )
        return encoded_access_token

    async def decode_token(self, token: str):
        """
        Decode a JWT token.

        This function decodes a JWT token and validates its scope.

        :param token: str: The JWT token to decode.
        :return: The payload of the decoded token.
        :rtype: dict
        :raises HTTPException: If the token is invalid.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "refresh_token":
                email = payload["email"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_SCOPE"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="NOT_VALIDATE_CREDENTIALS",
            )

    async def get_authenticated_user(
        self,
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ):
        """
        Get the authenticated user.

        This function retrieves the currently authenticated user using the provided token.

        :param token: str: The JWT token representing the user's authentication.
        :param db: AsyncSession: The database session.
        :return: The authenticated user.
        :rtype: User
        :raises HTTPException: If the token is invalid or the user is not found.
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="NOT_VALIDATE_CREDENTIALS"
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["email"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception

            # check token in blacklist
            is_invalid_token = await repository_users.is_blacklisted_token(token, db)
            if is_invalid_token:
                raise credentials_exception

        except jwt.InvalidTokenError:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception

        return user

    async def get_email_from_token(self, token: str):
        """
        Get the email address from an email verification token.

        This function decodes an email verification token and retrieves the email address from it.

        :param token: str: The JWT email verification token.
        :return: The email address.
        :rtype: str
        :raises HTTPException: If the token is invalid.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload["scope"] == "email_token":
                email = payload["email"]
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID_SCOPE"
            )
        except jwt.InvalidTokenError as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="FAIL_EMAIL_VERIFICATION",
            )


auth_service = Auth()
