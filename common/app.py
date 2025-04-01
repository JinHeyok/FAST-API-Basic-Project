import os
from dotenv import load_dotenv
from fastapi import *
from fastapi.openapi.utils import get_openapi

from enums.role import Role

# NOTE : FastAPI 인스턴스를 생성합니다
# NOTE : FastAPI 애플리케이션을 생성합니다. 이 인스턴스는 라우팅, 미들웨어, 요청 및 응답 처리 등을 담당합니다.
app = FastAPI()
ADMIN = Role.ADMIN.value
USER = Role.USER.value

# NOTE : .env 파일을 로드합니다
profile = os.getenv("PROFILE", "dev")
env_file = f".env.{profile}"
load_dotenv(env_file)
print(f"profile : {env_file}")


# NOTE : Swagger UI를 사용하기 위한 FastAPI 인스턴스를 생성합니다
# NOTE : custom_openapi 함수를 정의합니다. 이 함수는 OpenAPI 스키마를 커스터마이징하여 Swagger UI에서 JWT 토큰을 입력할 수 있도록 설정합니다.
def custom_openapi():
    # NOTE : 이미 생성된 OpenAPI 스키마가 있으면 그것을 반환합니다.
    if app.openapi_schema:
        return app.openapi_schema

    # NOTE : OpenAPI 스키마를 생성합니다. 여기에는 API의 제목, 설명, 버전 및 라우트 정보가 포함됩니다.
    openapi_schema = get_openapi(
        title="Fast API Test",  # NOTE : API의 제목
        description="FastAPI를 이용한 테스트 서버입니다.",  # NOTE : API의 설명
        version="1.0.0",  # NOTE : API의 버전
        routes=app.routes,  # NOTE : API의 라우트 정보
    )

    # NOTE : OpenAPI 스키마에 보안 스키마를 추가합니다. 여기서는 Bearer 토큰 인증을 사용합니다.
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",  # NOTE : 인증 타입은 HTTP입니다.
            "scheme": "bearer",  # NOTE : 인증 스키마는 Bearer입니다.
            "bearerFormat": "JWT",  # NOTE : Bearer 토큰의 형식은 JWT입니다.
        }
    }

    # NOTE : 모든 엔드포인트에 BearerAuth 보안 요구사항을 추가합니다.
    openapi_schema["security"] = [{"BearerAuth": []}]

    # NOTE : 생성된 OpenAPI 스키마를 FastAPI 애플리케이션에 설정합니다.
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# NOTE : FastAPI 애플리케이션의 OpenAPI 스키마를 커스터마이징된 스키마로 설정합니다.
app.openapi = custom_openapi



