from fastapi import FastAPI

from src.routes.user import router as user_router
from src.routes.url_create_redirect import router

app = FastAPI()


app.include_router(user_router)
app.include_router(router)