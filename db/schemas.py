from pydantic import BaseModel


class AuthorBase(BaseModel):
    id: int
    name: str
    bio: str
    
    class Config:
        from_attributes = True


class BookBase(BaseModel):
    id: int
    title: str
    pages: int
    author_id: int

    class Config:
        from_attributes = True
