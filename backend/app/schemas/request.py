from pydantic import BaseModel

class Query(BaseModel):
    topic: str