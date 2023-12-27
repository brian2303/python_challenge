from pydantic import BaseModel
from typing import List, Optional


class BookDTO(BaseModel):
    id: str
    title: str
    subtitle: str
    authors: List[str]
    categories: List[str]
    published_date: str
    editor: str
    description: str
    image: Optional[str]

    class Config:
        allow_population_by_field_name = True
