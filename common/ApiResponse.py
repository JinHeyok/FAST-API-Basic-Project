from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from common.app import app

"""
에러 발생시 JSON 형태로 응답을 반환하는 핸들러입니다.
"""
@app.exception_handler(HTTPException)
async def ApiResponse_Fail(request: Request, exc: HTTPException):
    detail_message = str(exc.detail).split(": ", 1)[-1] if ": " in str(exc.detail) else str(exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "status": "Fail", "message": f"{detail_message}"},
    )


"""
성공적인 응답을 반환하는 핸들러입니다.
"""
def ApiResponse_Success(data: dict, request: Request = None):
    return JSONResponse(
        status_code=200,
        content={"code": 200, "status": "Success", "data": data},
    )

