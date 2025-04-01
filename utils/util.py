from common.server import *

"""
클라이언트의 IP 주소를 가져오는 함수입니다.
"""
def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.client.host
    return client_ip
