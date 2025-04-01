from JWT.authentication import Authentication
from JWT.token import get_current_user
from common.server import *
from route.utils import setRouter

router = setRouter("/api/v1/test", "테스트 API")


@router.get("/",
            summary="테스트 ROOT API",
            description="""
### Test API root
Request 
```
Id : "고유 인덱스"
```
""")
def read_test(request: Request):
    return ApiResponse_Success({"test": "test"}, request)


@router.get("/userAuth",
            summary="사용자 권한 테스트 API",
            description="""
### 토큰 테스트 검증 API
### * JWT 필수
사용자의 권한을 검증한다.
""")
@Authentication([USER])
def userAuth(request: Request):
    user = get_current_user(request)
    return ApiResponse_Success(user, request)


@router.get("/adminAuth",
            summary="관리자 권한 테스트 API",
            description="""
### 토큰 테스트 검증 API
### * JWT 필수
사용자의 권한을 검증한다.
""")
@Authentication([ADMIN])
def adminAuth(request: Request):
    user = get_current_user(request)
    return ApiResponse_Success(user, request)
