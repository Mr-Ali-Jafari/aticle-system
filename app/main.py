from fastapi import FastAPI
from app.api.login import login
from app.models.models import Base
from app.api.user import user
from app.api.role import role
from app.config.database import database
from app.api.permission import permission
from app.utils.auth_jwt.auth import add_user_with_role_and_permission
from app.api.article import article
from app.config.database.database import SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os 


from dotenv import load_dotenv, dotenv_values 


load_dotenv(dotenv_path="app/")


Base.metadata.create_all(bind=database.engine)


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    add_user_with_role_and_permission(db,os.getenv('NAME') , os.getenv("EMAIL"), "12341234", os.getenv('ROLE') , os.getenv("PERMISSION"))
    db.close()


app.include_router(login.router)
app.include_router(permission.router)
app.include_router(user.router)
app.include_router(role.router)
app.include_router(article.router)




