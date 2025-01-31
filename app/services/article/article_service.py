import os
from sqlalchemy.orm import Session
from app.models.models import Article,User
from app.schemas.schemas import ArticleCreate, ArticleUpdate
from typing import Optional
from fastapi import UploadFile
from app.config.configs import MEDIA_DIR


UPLOAD_DIRECTORY = f"{MEDIA_DIR}/uploads/"

os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    """
    Save an uploaded file to the upload directory and return its path.
    """
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    return file_path


def create_article(
    db: Session,
    article: ArticleCreate,
    image: Optional[UploadFile] = None 
):
    image_url = None
    image_filename = None

    if image:
        file_path = save_uploaded_file(image)
        image_url = file_path  
        image_filename = image.filename

    db_article = Article(
        title=article.title,
        content=article.content,
        image_url=image_url,
        image_filename=image_filename,
        author_id=article.author_id,
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(
    db: Session,
    article_id: int,
    article: ArticleUpdate,
    image: Optional[UploadFile] = None 
):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:
        db_article.title = article.title
        db_article.content = article.content

        if image:

            file_path = save_uploaded_file(image)
            db_article.image_url = file_path 
            db_article.image_filename = image.filename

        db.commit()
        db.refresh(db_article)
        return db_article
    return None


def delete_article(db: Session, article_id: int):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if db_article:

        if db_article.image_url and os.path.exists(db_article.image_url):
            os.remove(db_article.image_url)

        db.delete(db_article)
        db.commit()
        return True
    return False


def get_article(db: Session, article_id: int):
    return db.query(Article).filter(Article.id == article_id).first()


def get_articles(db: Session):
    return db.query(Article).all()


def search_articles(db: Session, query: Optional[str] = None):
    query_filter = db.query(Article)
    
    if query:
        query_filter = query_filter.filter(Article.title.ilike(f"%{query}%") | Article.content.ilike(f"%{query}%"))
    
    return query_filter.all()



def get_authors(db: Session):

    authors = db.query(User).filter(User.id == Article.id).first()
    return authors


def get_authors_by_username(db: Session, query: Optional[str] = None):
    query_filter = db.query(User).filter(User.id == Article.id)
    
    if query:
        query_filter = query_filter.filter(User.username.ilike(f"%{query}%"))
    


    return query_filter.all()