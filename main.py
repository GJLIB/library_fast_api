from fastapi import FastAPI, Query

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

@app.get('/all_books')
def get_all_books():
    return library