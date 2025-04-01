from inspect import Parameter

from sqlalchemy.orm import joinedload

from JWT.token import *
from common.server import *
from model import models
from model.dbConnection import Session, save_to_db, update_to_db
from model.request.userRequest import UserRequest
from route.utils import setRouter

router = setRouter("/api/v1/auth", "인증 API")


@router.post("/login",
             summary="로그인 API",
             description="""
### 로그인 API
### 로그인 API입니다.
```
username : "고유 인덱스"
```
""")
def login(request: Request,
          username: str = Body("username", description="회원의 아이디", example="아이디"),
          password: str = Body("password", description="회원의 비밀번호", example="비밀번호")):
    """
    로그인 API
    """
    # 로그인 처리
    # 예시: 사용자 인증, 토큰 생성 등
    # 성공적인 로그인 후 응답 반환
    # JWT 토큰 생성
    access_token = create_access_token(username, [ADMIN])
    response = {"access_token": access_token, "token_type": "bearer", "roles": [ADMIN]}
    return ApiResponse_Success(response, request)


@router.post("/registration",
             summary="회원가입 API",
             description="""
### 회원가입 API
### 회원가입 API 입니다.
---
## Request Body
```json
{
  "username": "아이디",
  "password": "비밀번호",
  "name": "이름"
}
```    
""")
def userRegistration(request: Request, user_request: UserRequest):
    """
    회원가입 API
    # 회원가입 처리
    # 예시: 사용자 정보 저장, 비밀번호 해싱 등
    # 성공적인 회원가입 후 응답 반환
    """
    session = Session()
    try:
        if session.query(models.User).filter(models.User.u_username == user_request.username).first():
            raise HTTPException(status_code=500, detail=ErrorMessage.USERNAME_ALREADY.value)
        user = models.User(u_username=user_request.username,
                           u_password=user_request.password,
                           u_name=user_request.name,
                           tasks=[models.Task(t_title=task.title) for task in user_request.tasks]
                           )
        user = save_to_db(session, user)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    response = user.as_dict(["password", "title"])
    return ApiResponse_Success(response, request)


@router.get("/{id}",
            summary="회원정보 단일 데이터 조회 API",
            description="""
### 회원정보 단일 데이터 조회 API
### 회원정보 단일 데이터 조회 API입니다.
---
## Request Param
```json
"id": "회원 고유 인덱스"
```    
""")
def getUser(request: Request,
            id: int = Path(..., description="회원 고유 인덱스", example=1)):
    """
    회원정보 단일 데이터 조회 API
    # 회원정보 단일 데이터 조회 처리
    # 예시: 사용자 정보 조회 등
    # 성공적인 회원정보 단일 데이터 조회 후 응답 반환
    """
    session = Session()
    try:
        user = (session.query(models.User)
                .filter(models.User.u_id == id)
                .options(joinedload(models.User.tasks)).first())
        if not user:
            raise HTTPException(status_code=404, detail=ErrorMessage.USER_NOT_FOUND.value)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    response = user.as_dict(["password"])
    return ApiResponse_Success(response, request)


@router.put("/{id}",
            summary="회원정보 수정 API",
            description="""
### 회원정보 수정 API
### 회원정보 수정 API입니다.
---
## Request Param
```json 
"id": "회원 고유 인덱스"
```
## Request Body
```json
{
  "username": "아이디",
  "password": "비밀번호",
  "name": "이름"
}
```
""")
def updateUser(request: Request,
               user_request: UserRequest,
               id: int = Path(..., description="회원 고유 인덱스", example=1)):
    """
    회원정보 수정 API
    # 회원정보 수정 처리
    # 예시: 사용자 정보 수정 등
    # 성공적인 회원정보 수정 후 응답 반환
    """
    session = Session()
    try:
        user = session.query(models.User).filter(models.User.u_id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail=ErrorMessage.USER_NOT_FOUND.value)
        if user_request.username is not None and session.query(models.User).filter(
                models.User.u_username == user_request.username).first():
            raise HTTPException(status_code=500, detail=ErrorMessage.USERNAME_ALREADY.value)
        update_to_db(session, user, user_request)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()
    response = user.as_dict(["password"])
    return ApiResponse_Success(response, request)
