from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from model.dbConnection import Base


class User(Base):
    __tablename__ = 'user'
    u_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_username = Column(String(100), nullable=False, index=True)
    u_password = Column(String(255), nullable=False, index=True)
    u_name = Column(String(100), nullable=False, index=True)
    tasks = relationship("Task", back_populates="user")  # task 테이블과의 관계 설정


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    u_id = Column(Integer, ForeignKey('user.u_id', ondelete='CASCADE', onupdate="CASCADE"))  # user 테이블과의 외래키 설정
    user = relationship("User", back_populates="tasks")  # user 테이블과의 관계 설정
    t_title = Column(String(255), index=True)  # task 제목
