from enum import Enum


class ErrorMessage(Enum):
    PERMISSION_NOT_FOND = "접근 권한이 존재하지 않습니다."
    PERMISSION_NECESSARY = "접근 권한이 필요합니다."
    TOKEN_HAS_EXPIRED = "토큰이 만료되었습니다."
    INVALID_TOKEN = "유효하지 않은 토큰입니다."
    USER_NOT_FOUND = "사용자를 찾을 수 없습니다."
    DB_CONNECTION_FAILED = "데이터베이스 연결에 실패했습니다."
    USERNAME_ALREADY = "이미 사용중인 아이디입니다."