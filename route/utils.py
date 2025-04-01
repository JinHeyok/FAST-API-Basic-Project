from fastapi import APIRouter

"""
: FastAPI 라우터를 생성하는 헬퍼 함수입니다.
: @param prefix: 라우터의 URL prefix
: @param tags: 라우터의 태그
"""
def setRouter(prefix: str, tags: str):
    router = APIRouter(prefix=prefix, tags=[tags])
    return router
