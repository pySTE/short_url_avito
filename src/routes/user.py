from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database.connection import get_db
from src.schemas.user import User
from src.models.user import User as UserDb
from src.utils.encrypt_password import create_hash
from src.utils.jwt_handler import create_access_token

router = APIRouter(prefix="/user")


@router.post('/login')
async def login(user_data: User, db: AsyncSession = Depends(get_db)):
    user_find = await db.execute(select(UserDb).where(user_data.email == UserDb.email))
    user_find = user_find.scalars().first()
    if user_find:
        if create_hash(user_data.password) == user_find.password:
            token_jwt = create_access_token(user_data.email)
            return {
                "access_token": token_jwt,
                "token_type": "Bearer"
            }
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post('/register')
async def register(user_data: User, db: AsyncSession = Depends(get_db)):
    user_find = await db.execute(select(UserDb).where(user_data.email == UserDb.email))
    user_find = user_find.scalars().first()
    if user_find:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    else:
        password = create_hash(user_data.password)
        user_data_for_db = UserDb(
            email=user_data.email,
            password=password
        )
        db.add(user_data_for_db)
        await db.commit()
        jwt_token = create_access_token(user_data.email)
        return {
                "access_token": jwt_token,
                "token_type": "Bearer"
            }
