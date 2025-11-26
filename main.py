from fastapi import FastAPI

from routes.user import router as user_router
from routes.url_create_redirect import router

app = FastAPI()


app.include_router(user_router)
app.include_router(router)