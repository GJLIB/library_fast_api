from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

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

@app.post("/token")
async def token_create(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data = db.query(models.User).filter()
    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    global user
    user = models.User(**user_data)
    
    return {"access_token": user.username, "token_type": "bearer"}


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


@app.post('/ad_book') 
async def add_book(author: str = Query(..., min_length = 4, max_length = 20, title = "Author's name"),
                title: str = Query(..., min_length = 2, max_lenght = 100, title = "Book title"),
                pages: int = Query(..., gt = 10, title = "Number of pages")):
        
    if author not in library:
        library[author] = []
    library[author].append({"title": title, "pages": pages})
    return {"message": "Book added successfully."}

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
    