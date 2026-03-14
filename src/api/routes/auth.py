"""Auth: register, login, me."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.schemas import UserCreate, UserLogin, Token, UserResponse
from src.api.deps import (
    get_db,
    get_password_hash,
    create_access_token,
    verify_password,
    CurrentUser,
)
from src.db.models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _validate_password(password: str) -> None:
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")


@router.post("/register", response_model=UserResponse)
def register(data: UserCreate, db=Depends(get_db)):
    _validate_password(data.password)
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(
        username=data.username,
        password_hash=get_password_hash(data.password),
        role=data.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(data: UserLogin, db=Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(data={"sub": str(user.id)})
    return Token(access_token=token)


@router.get("/me", response_model=UserResponse)
def me(current_user: CurrentUser):
    return current_user
