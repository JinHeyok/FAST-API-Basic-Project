from common.server import *
from model import dbConnection, models


@app.get("/")
def read_root():
    return {"Hello": "World"}


# NOTE : Controller에 있는 Router API를 가져와서 FastAPI 앱에 등록
for router in routesList:
    app.include_router(router)

# NOTE : 데이터베이스 연결
# dbConnection.Base.metadata.drop_all(bind=dbConnection.engine)
dbConnection.Base.metadata.create_all(bind=dbConnection.engine)

if __name__ == '__main__':
    uvicorn.run(app, port=5700, host='127.0.0.1')
