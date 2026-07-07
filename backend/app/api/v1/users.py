from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate
from app.services.user import create_user

from app.schemas.user import UserLogin
from app.services.user import authenticate_user
from app.core.security import create_access_token
from fastapi import HTTPException

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)

    return {
        "message": "User created successfully",
        "username": new_user.username,
        "email": new_user.email,
    }

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and return JWT token.
    """

    user = authenticate_user(
        db,
        user_data.email,
        user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={"sub": user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }