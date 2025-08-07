from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from db import models, schemas
from db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

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

