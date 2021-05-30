from sqlalchemy import Column, Integer, String, create_engine, orm, func, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random as rnd

engine = create_engine(
    'postgresql://lnjyvgunefntkt:fb5960233911d07deae3dfed28656a038c4af868a9996c49c736e560e5f01765@ec2-3-233-7-12.compute-1.amazonaws.com:5432/d86uabp7ikq67s')
Base = declarative_base()
session = sessionmaker(bind=engine)()
session.begin(subtransactions=True)


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    rate = Column(String, default=-1)


Base.metadata.create_all(engine)


def get_user(user_id: int) -> User:
    return session.query(User).filter_by(user_id=user_id).first()


def edit_user(user_id: int, **kwargs):
    user = get_user(user_id)
    session.delete(user)
    for key, value in kwargs.items():
        user.__setattr__(key, value)
    session.add(user)
    session.commit()


def new_user(user_id: int):
    if get_user(user_id):
        return
    session.add(User(user_id=user_id))
    session.commit()
