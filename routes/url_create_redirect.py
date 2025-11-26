from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from utils.generate import generate_unique_id
from models.url import Urls
from utils.jwt_handler import verify_access_token
from config import MAIN_URL

router = APIRouter()


@router.post("/create_url")
async def create_url(url: str, token: str | None, db: AsyncSession = Depends(get_db)):
    try:
        email = verify_access_token(token).get('user')
    except Exception as e:
        email = None
    new_url = await generate_unique_id()
    if email:
        url_model = Urls(new_url=new_url, url=url, email=email)
    else:
        url_model = Urls(new_url=new_url, url=url)
    db.add(url_model)
    await db.commit()
    return {"url": f"{MAIN_URL}/red/{new_url}"}


@router.get("/red/{new_url}")
async def redirect_url(new_url: str, db: AsyncSession = Depends(get_db)):
    exciting_url = await db.execute(select(Urls).where(Urls.new_url == new_url))
    exciting_url = exciting_url.scalars().first()
    redirect_url_old = exciting_url.url
    if exciting_url:
        return RedirectResponse(redirect_url_old)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/all_urls')
async def get_all_urls(token: str, db: AsyncSession = Depends(get_db)):
    email = verify_access_token(token).get('user')
    if email:
        all_urls = await db.execute(select(Urls.new_url).where(Urls.email == email))    # Expected type 'ColumnElement[bool] | _HasClauseElement[bool] | SQLCoreOperations[bool] | ExpressionElementRole[bool] | TypedColumnsClauseRole[bool] | () -> ColumnElement[bool] | LambdaElement', got 'bool' instead
        all_urls = all_urls.scalars().all()
        for i in range(len(all_urls)):
            all_urls[i] = f"{MAIN_URL}/red/{all_urls[i]}"    # Class 'Sequence' does not define '__setitem__', so the '[]' operator cannot be used on its instances
        return {"urls": all_urls}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
