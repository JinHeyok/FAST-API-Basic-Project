from fastapi import HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone

from enums.errorMessage import ErrorMessage

# NOTE : JWT 비밀 키를 설정합니다
SECRET_KEY = "ninefive"
# NOTE : JWT 알고리즘을 설정합니다
ALGORITHM = "HS256"
# NOTE : 액세스 토큰의 만료 시간을 설정합니다 (분 단위)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# NOTE : OAuth2PasswordBearer 인스턴스를 생성합니다. 이 인스턴스는 토큰 URL을 사용하여 OAuth2 인증을 처리합니다.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# NOTE : 액세스 토큰을 생성하는 함수입니다
def create_access_token(username: str, roles: list = None):
    # NOTE : 토큰의 만료 시간을 설정합니다
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # NOTE : 토큰에 포함될 데이터를 설정합니다
    data = {"username": username, "roles": roles, "exp": expire}
    to_encode = data.copy()
    # NOTE : JWT 토큰을 생성합니다
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# NOTE : 액세스 토큰을 검증하는 함수입니다
def verify_access_token(token: str):
    try:
        # NOTE : JWT 토큰을 디코딩하여 페이로드를 반환합니다
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # NOTE : 토큰이 만료된 경우 예외를 발생시킵니다
        raise HTTPException(status_code=401, detail=ErrorMessage.TOKEN_HAS_EXPIRED.value)
    except jwt.InvalidTokenError:
        # NOTE : 토큰이 유효하지 않은 경우 예외를 발생시킵니다
        raise HTTPException(status_code=401, detail=ErrorMessage.INVALID_TOKEN.value)


# NOTE : 현재 사용자의 권한을 검사하는
def user_role_require(request: Request, roleList: list = None):
    # NOTE : 자격 증명 예외를 설정합니다
    credentials_exception = HTTPException(
        status_code=401,
        detail=ErrorMessage.PERMISSION_NOT_FOND.value,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # NOTE : 요청 헤더에서 Authorization 토큰을 가져옵니다
        token = request.headers.get("Authorization")
        if token is None or not token.startswith("Bearer "):
            raise credentials_exception
        if not token.startswith("Bearer "):
            raise credentials_exception
        # NOTE : 토큰에서 "Bearer " 부분을 제거합니다
        token = token[len("Bearer "):]
        # NOTE : 토큰을 검증하여 페이로드를 가져옵니다
        payload = verify_access_token(token)
        # NOTE : 페이로드에서 사용자 이름과 역할을 가져옵니다
        username: str = payload.get("username")
        roles: list = payload.get("roles")
        response = {"username": username, "roles": roles}

        if username is None or roles is None:
            raise credentials_exception
        # NOTE : 역할 목록이 제공된 경우, 사용자가 해당 역할을 가지고 있는지 확인합니다
        if roleList and not any(role in roles for role in roleList):
            raise HTTPException(
                status_code=403,
                detail=ErrorMessage.PERMISSION_NECESSARY.value,
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception


# NOTE : 토크은으로 현재 사용자를 가져온다.
def get_current_user(request: Request):
    # NOTE : 자격 증명 예외를 설정합니다
    credentials_exception = HTTPException(
        status_code=401,
        detail=ErrorMessage.PERMISSION_NOT_FOND.value,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # NOTE : 요청 헤더에서 Authorization 토큰을 가져옵니다
        token = request.headers.get("Authorization")
        if not token.startswith("Bearer "):
            raise credentials_exception
        # NOTE : 토큰에서 "Bearer " 부분을 제거합니다
        token = token[len("Bearer "):]
        # NOTE : 토큰을 검증하여 페이로드를 가져옵니다
        payload = verify_access_token(token)

        # NOTE : 페이로드에서 사용자 이름과 역할을 가져옵니다
        username: str = payload.get("username")
        roles: list = payload.get("roles")
        response = {"username": username, "roles": roles}

        if username is None:
            raise credentials_exception
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    return response
