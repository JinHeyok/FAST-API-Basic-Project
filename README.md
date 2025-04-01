## 📌 FAST API Basic Project
### 🧑‍💻 작성자 : JinHyeok

---

## 📌Confiuguration

---

|     항목     |  Version   |            비고            |
|:----------:|:----------:|:------------------------:|
| **Python** |    3.12    |
| **MySQL**  |   8.0.33   | Connection lib : pymysql |
|  **ORM**   | sqlalchemy |

- [ ]  **FastAPI** :  FastAPI는 Python으로 작성된 현대적인 웹 프레임워크입니다. 빠르고, 간단하며, 비동기 프로그래밍을 지원합니다.
- [ ]  **uvicorn** :  FastAPI 애플리케이션을 실행하기 위한 ASGI 서버입니다. 비동기 처리를 지원하며, 높은 성능을 자랑합니다.
- [ ]  **pydantic** :  데이터 검증 및 설정 관리를 위한 라이브러리입니다. FastAPI와 함께 사용되어 요청 및 응답 데이터의 유효성을 검사합니다.
- [ ]  **sqlalchemy** :  Python SQL Toolkit 및 ORM입니다. 데이터베이스와의 상호작용을 쉽게 만들어줍니다.
- [ ]  **pymysql** :  MySQL 데이터베이스와의 연결을 위한 라이브러리입니다. SQLAlchemy와 함께 사용됩니다.
- [ ]  **python-dotenv** :  환경 변수를 관리하기 위한 라이브러리입니다. .env 파일을 사용하여 환경 변수를 쉽게 설정할 수 있습니다.

--- 

## 📌 Project Common Function

---

### 1. **DB Connection**

    ✅ path : model/dbConnection.py
    ✅ DB Connection을 위한 SQLAlchemy 엔진을 생성하는 함수입니다.
    ✅ DB CRUD 작업을 수행하기 위한 함수가 정의 되어있습니다.

### 2. **DB Model**

    ✅ path : model/dbModel.py
    ✅ SQLAlchemy ORM 모델을 정의하는 파일입니다. 데이터베이스 테이블과 매핑되는 클래스를 정의합니다.

### 3. **Api Response**

    ✅ path : common/*.py
    ✅ API 응답을 위한 Pydantic 모델을 정의하는 파일입니다. 요청 및 응답 데이터의 유효성을 검사합니다.
    ✅ FastAPI 애플리케이션을 실행하는 파일입니다.
    ✅ .env 파일을 로드하여 환경 변수를 설정합니다.
    ✅ Swagger UI를 사용하여 API 문서를 자동으로 생성합니다.
    ✅ server.py FAST API의 모듈을 사용하기 위한 파일입니다.

### 4. **Router**

    ✅ path : route/*.py
    ✅ FastAPI 라우터를 정의하는 파일입니다.

### 5.**JWT**

    ✅ path : JWT/*.py
    ✅ JWT 토큰을 생성하고 검증하는 함수가 정의되어 있습니다.
    ✅ JWT를 사용하여 인증 및 인가를 처리합니다.

### 6. **enum**

    ✅ path : enums/*.py
    ✅ 공통으로 사용할 Enum 클래스를 정의하는 파일입니다.
    ✅ 에러 메시지를 정의하는 Enum 클래스를 정의합니다.
    ✅ User의 권한을 정의하는 Enum 클래스를 정의합니다.

### 7. **Controller**

    ✅ path : controller/*.py
    ✅ API 요청을 처리하는 비즈니스 로직을 정의하는 파일입니다. 
    ✅ 각 API 요청에 대한 핸들러 함수를 정의합니다.
