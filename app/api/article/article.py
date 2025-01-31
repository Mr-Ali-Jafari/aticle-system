from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, Request,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.config.database.database import get_db
from app.schemas.schemas import ArticleCreate, ArticleUpdate,UserBase
from app.services.article.article_service import get_authors_by_username,get_authors,create_article, update_article,search_articles, delete_article, get_article, get_articles
from typing import List, Optional
from app.config.configs import BASE_DIR
from app.schemas import schemas
# static files
from app.api.login.login import get_current_user
# Initialize the router and templates
router = APIRouter(
    prefix="/article",
    tags=["Article"],
    responses={404: {"description": "Not found"}},
)





# Create an article with an optional image upload
@router.post("/articles/", response_model=ArticleCreate)
async def create_article_endpoint(
    title: str = Form(...),
    content: str = Form(...),
    author_id: schemas.User = Depends(get_current_user),
    image: UploadFile = None,
    db: Session = Depends(get_db),
):
    article_data = ArticleCreate(title=title, content=content, author_id=author_id.id)
    return create_article(db, article=article_data, image=image)

# HTML Route: Form to update an article

# Update an existing article with optional image upload
@router.put("/articles/{article_id}/", response_model=ArticleUpdate)
async def update_article_endpoint(
    article_id: int,
    title: Optional[str] = Form(None),
    content: Optional[str] = Form(None),
    image: UploadFile = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    article_data = ArticleUpdate(title=title, content=content)
    updated_article = update_article(db, article_id=article_id, article=article_data, image=image)
    
    if not updated_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article


# Delete an article
@router.post("/articles/{article_id}/")
async def delete_article_endpoint(article_id: int, db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    deleted = delete_article(db, article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted successfully"}



# search article api

@router.get("/search/")
def search(db: Session = Depends(get_db), query: Optional[str] = None,current_user: schemas.User = Depends(get_current_user)):
    return search_articles(db=db,query=query)


# get articles

@router.get('/get/all/')
def get_all(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    return get_articles(db=db)


@router.get('/get/all/authors/',response_model=UserBase)
def get_all_authors(db: Session = Depends(get_db),current_user: schemas.User = Depends(get_current_user)):
    return get_authors(db=db)


@router.get("/search/authors/")
def search_authors(db: Session = Depends(get_db), query: Optional[str] = None,current_user: schemas.User = Depends(get_current_user)):
    return get_authors_by_username(db=db,query=query)