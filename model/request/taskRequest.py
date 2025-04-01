from pydantic import BaseModel, Field

class taskRequest(BaseModel):
    title: str = Field(..., example="제목")

    class Config:
        schema_extra = {
            "example": {
                "title": "제목"
            }
        }
