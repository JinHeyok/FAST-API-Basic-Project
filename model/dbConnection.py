from datetime import datetime

from pyodbc import OperationalError
from sqlalchemy import DateTime, func , Column
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import DetachedInstanceError

from common.server import *

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

print("Connecting to database...")

# NOTE :  데이터베이스 URL 설정
DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
print(DATABASE_URL)

# NOTE :  SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)
# NOTE :  SQLAlchemy 세션 생성
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# NOTE :  SQLAlchemy 기본 모델 클래스 생성
Base = declarative_base()


@as_declarative()
class Base:
    # NOTE : 클래스 이름을 소문자로 변환하여 테이블 이름으로 사용
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    createdAt = Column(DateTime, default=func.now(), nullable=False)
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # NOTE : exclude_columns 속성을 사용하여 제외할 열을 지정
    def as_dict(self, exclude_columns=None, session: Session = None):
        # NOTE : exclude_columns가 None이면 빈 리스트로 초기화
        if exclude_columns is None:
            exclude_columns = []
        result = {}
        # NOTE : 테이블의 모든 열에 대해 반복
        for c in self.__table__.columns:
            # NOTE : 열 이름에서 첫 번째 언더스코어 이후의 부분을 키로 사용
            key = c.name.split('_', 1)[-1] if '_' in c.name else c.name
            # NOTE : 제외할 열이 아니면
            if key not in exclude_columns:
                value = getattr(self, c.name)
                # NOTE : 값이 datetime 타입이면 문자열로 변환
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                result[key] = value

        # NOTE : 연관된 관계를 포함
        for relationship in self.__mapper__.relationships:
            # NOTE : 제외할 열이 아니면
            if relationship.key not in exclude_columns:
                try:
                    # NOTE : 관계된 값을 가져옴
                    related_value = getattr(self, relationship.key)
                    if related_value is not None:
                        # NOTE : 관계된 값이 리스트인 경우
                        if isinstance(related_value, list):
                            # NOTE : 리스트의 각 항목에 대해 as_dict 호출
                            result[relationship.key] = [item.as_dict(exclude_columns=exclude_columns, session=session)
                                                        for item in related_value]
                        else:
                            # NOTE : 관계된 값이 리스트가 아닌 경우 as_dict 호출
                            result[relationship.key] = related_value.as_dict(exclude_columns=exclude_columns,
                                                                             session=session)
                except DetachedInstanceError:
                    if session:
                        # NOTE : 세션에서 관계된 값을 가져옴
                        related_value = session.query(relationship.mapper.class_).get(
                            getattr(self, relationship.local_columns[0].name))
                        if related_value is not None:
                            if isinstance(related_value, list):
                                # NOTE : 리스트의 각 항목에 대해 as_dict 호출
                                result[relationship.key] = [
                                    item.as_dict(exclude_columns=exclude_columns, session=session) for item in
                                    related_value]
                            else:
                                # NOTE : 관계된 값이 리스트가 아닌 경우 as_dict 호출
                                result[relationship.key] = related_value.as_dict(exclude_columns=exclude_columns,
                                                                                 session=session)
                    else:
                        # NOTE : 세션이 없는 경우 None으로 설정
                        result[relationship.key] = None
        return result


# NOTE : DB 연결 테스트
def connection_test():
    try:
        # NOTE : 데이터베이스 연결 테스트
        connection = engine.connect()
        print("Database connection successful!")
        connection.close()
    except OperationalError as e:
        print(f"Database connection failed: {e}")


# NOTE : DB 데이터 생성 함수
def save_to_db(session: Session, instance):
    """
    주어진 인스턴스를 데이터베이스에 저장합니다.
    """
    try:
        session.add(instance)  # NOTE : 인스턴스를 세션에 추가
        session.commit()  # NOTE : 변경 사항을 커밋
        session.refresh(instance)  # NOTE : 인스턴스를 세션에 바인딩

        # NOTE : 인스턴스의 관계를 동적으로 처리하여 세션에 추가
        for relationship in instance.__mapper__.relationships:
            related_value = getattr(instance, relationship.key)  # NOTE : 관계된 값을 가져옴
            if related_value is not None:  # NOTE : 관계된 값이 None이 아닌 경우
                if isinstance(related_value, list):  # NOTE : 관계된 값이 리스트인 경우
                    for item in related_value:  # NOTE : 리스트의 각 항목에 대해
                        session.add(item)  # NOTE : 세션에 항목을 추가
                else:  # NOTE : 관계된 값이 리스트가 아닌 경우
                    session.add(related_value)  # NOTE : 세션에 관계된 값을 추가
        session.commit()  # NOTE : 변경 사항을 커밋

        # NOTE : 인스턴스의 관계를 동적으로 처리하여 세션에서 갱신
        for relationship in instance.__mapper__.relationships:
            related_value = getattr(instance, relationship.key)  # NOTE : 관계된 값을 가져옴
            if related_value is not None:  # NOTE : 관계된 값이 None이 아닌 경우
                if isinstance(related_value, list):  # NOTE : 관계된 값이 리스트인 경우
                    for item in related_value:  # NOTE : 리스트의 각 항목에 대해
                        session.refresh(item)  # NOTE : 세션에서 항목을 갱신
                else:  # NOTE : 관계된 값이 리스트가 아닌 경우
                    session.refresh(related_value)  # NOTE : 세션에서 관계된 값을 갱신

        return instance  # NOTE : 인스턴스를 반환
    except Exception as e:
        session.rollback()  # NOTE : 오류 발생 시 롤백
        raise HTTPException(status_code=500, detail=str(e))  # NOTE : HTTP 예외 발생
    finally:
        session.close()  # NOTE : 세션 닫기


# NOTE : DB 데이터 삭제 함수
def delete_to_db(session: Session, instance):
    """
    주어진 인스턴스를 데이터베이스에서 삭제합니다.
    """
    try:
        session.delete(instance)  # NOTE : 인스턴스를 세션에서 삭제
        session.commit()  # NOTE : 변경 사항을 커밋
        return True  # NOTE : 삭제 성공 시 True 반환
    except Exception as e:
        session.rollback()  # NOTE : 오류 발생 시 롤백
        raise HTTPException(status_code=500, detail=str(e))  # NOTE : HTTP 예외 발생
    finally:
        session.close()  # NOTE : 세션 닫기


# NOTE : DB 데이터 업데이트 함수
def update_to_db(session: Session, instance, updateInstance):
    """
    주어진 인스턴스를 데이터베이스에서 업데이트합니다.

    :param session: SQLAlchemy 세션
    :param instance: 업데이트할 인스턴스
    :param updateInstance: 업데이트할 값이 포함된 인스턴스
    """
    try:
        # instance와 updateInstance를 dict 형태로 변환
        instance_dict = {key.split('_', 1)[-1] if '_' in key else key: key for key in instance.__dict__.keys()}
        update_dict = updateInstance.__dict__ if hasattr(updateInstance, '__dict__') else updateInstance

        # update_dict의 키 값을 사용하여 instance의 값을 수정
        for key, value in update_dict.items():
            if key in instance_dict and value is not None:
                setattr(instance, instance_dict[key], value)

        # instance가 SQLAlchemy 모델 인스턴스인지 확인
        if not hasattr(instance, '_sa_instance_state'):
            raise ValueError("instance는 SQLAlchemy 모델 인스턴스여야 합니다.")

        session.merge(instance)  # 인스턴스를 세션에 병합
        session.commit()  # 변경 사항을 커밋
        session.refresh(instance)  # 인스턴스를 세션에 바인딩

        return instance  # 인스턴스를 반환
    except Exception as e:
        session.rollback()  # 오류 발생 시 롤백
        raise HTTPException(status_code=500, detail=str(e))  # HTTP 예외 발생
    finally:
        session.close()  # 세션 닫기
