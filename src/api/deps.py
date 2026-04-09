"""FastAPI dependencies: DB session, current user, optional auth."""

import hashlib
import os
import secrets
from typing import Annotated, Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.db.database import SessionLocal, init_db
from src.db.models import User

# P-02: JWT security hardening
_SECRET_KEY_FALLBACK = "dev-secret-change-in-production"
SECRET_KEY = os.environ.get("SECRET_KEY", _SECRET_KEY_FALLBACK)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

security = HTTPBearer(auto_error=False)


def _hash_password(password: str, salt: str) -> str:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000).hex()


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed or ":" not in hashed:
        return False
    salt, stored = hashed.split(":", 1)
    return secrets.compare_digest(_hash_password(plain, salt), stored)


def get_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    h = _hash_password(password, salt)
    return f"{salt}:{h}"


def create_access_token(data: dict) -> str:
    from datetime import datetime, timedelta, timezone
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


async def get_current_user_optional(
    db: DbSession,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> User | None:
    if not credentials:
        return None
    payload = decode_token(credentials.credentials)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(User).filter(User.id == int(user_id)).first()
    return user


async def get_current_user(
    user: User | None = Depends(get_current_user_optional),
) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentUserOptional = Annotated[User | None, Depends(get_current_user_optional)]
