from fastapi import APIRouter, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import schemas as schemas
from app.config.database.database import get_db
from app.services.login.login_service import (
    login_for_access_token_service,
    get_current_user_service,
)
from app.config.configs import BASE_DIR
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/login",
    tags=['Login']
)
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")






oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        return login_for_access_token_service(db, form_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/current-user", response_model=schemas.User)
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_current_user_service(db, token)


@router.get("/login", response_class=HTMLResponse)
async def render_login_page(request: Request):

    return templates.TemplateResponse("login.html", {"request": request})