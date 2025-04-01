# JWT/authentication.py
import inspect
from functools import wraps

from fastapi import Request

from JWT.token import user_role_require


# NOTE: 역할 기반 접근 제어를 위한 데코레이터 함수입니다.
def Authentication(roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # NOTE: 현재 사용자를 가져와 역할을 확인합니다.
            user = user_role_require(request, roles)
            # NOTE: 함수가 비동기 함수인지 확인하고, 비동기 함수인 경우 await를 사용합니다.
            if inspect.iscoroutinefunction(func):
                return await func(request, *args, **kwargs)
            else:
                return func(request, *args, **kwargs)

        return wrapper

    return decorator
