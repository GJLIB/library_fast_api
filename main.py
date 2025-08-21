from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Annotated

SECRET_KEY = "19109197bd5e7c289b92b2b355083ea26c71dee2085ceccc19308a7291b2ea06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def token_create(data: dict):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

@app.post("/token")
async def token_get(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter(models.User.username == form_data.username,
    models.User.password == form_data.password).first()

    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = token_create(data = {'sub': user_data.username})
    
    return {"access_token": token, "token_type": "bearer"}


library = {
    'Ліна Костенко': [
        {'title': "Маруся Чурай", 'pages': 220},
        {'title': "Записки українського самашедшого", 'pages': 300}
    ],
    'Тарас Шевченко': [
        {'title': "Кобзар", 'pages': 350},
        {'title': "Гайдамаки", 'pages': 180}
    ],
    'Іван Франко': [
        {'title': "Захар Беркут", 'pages': 240},
        {'title': "Мойсей", 'pages': 170}
    ],
    'Леся Українка': [
        {'title': "Лісова пісня", 'pages': 120},
        {'title': "На крилах пісень", 'pages': 200}
    ]
}


@app.post('/add_book') 
async def add_book(token: Annotated[str, Depends(oauth2_scheme)],
                   db: Session = Depends(get_db),
                   author_name: str = Query(..., min_length = 4, max_length = 20, title = "Author's name"),
                   title: str = Query(..., min_length = 2, max_lenght = 100, title = "Book title"),
                   pages: int = Query(..., gt = 10, title = "Number of pages")):
        
    author = db.query(models.Author).filter_by(name = author_name).first()
    if not author:
        author = models.Author(name = author_name)
        db.add(author)
        db.commit()
        db.refresh(author)
    book = models.Book(title = title, pages = pages, author_id = author.id)
    db.add(book)
    db.commit()
    db.refresh(book)
    
    return {'message': 'Book added successfully.', 'book': book}

@app.get('/all_books', response_model = list[schemas.BookBase])
def get_all_books(db:Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

@app.get('/author/{author_name}')
async def get_books_author(author_name: str, db: Session = Depends(get_db)):
    if author_name in library:
        author = db.query(models.Author).filter_by(name = author_name).first()
        if author:
            books = db.query(models.Book).filter_by(author_id = author.id).all()
            return {author_name: books}
    else:
        return{'message': 'author not found in the library'}
    