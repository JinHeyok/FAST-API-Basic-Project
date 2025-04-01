from pydantic import BaseModel, Field
from typing import List, Optional
from model.request.taskRequest import taskRequest

class UserRequest(BaseModel):
    username: Optional[str] = Field(None, example="아이디")
    password: Optional[str] = Field(None, example="비밀번호")
    name: Optional[str] = Field(None, example="이름")
    tasks: List[taskRequest] = Field(None, example=[{"title": "제목"}])

    class Config:
        schema_extra = {
            "example": {
                "username": "아이디",
                "password": "비밀번호",
                "name": "이름",
                "tasks": [{"title": "제목"}]
            }
        }