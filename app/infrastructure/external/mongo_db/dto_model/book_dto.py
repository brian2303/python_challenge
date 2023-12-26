from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BookDTO(BaseModel):
    _id: str
    title: str
    subtitle: str
    authors: List[str]
    categories: List[str]
    publication_date: datetime
    editor: str
    description: str
    image: Optional[str]

    class Config:
        allow_population_by_field_name = True
