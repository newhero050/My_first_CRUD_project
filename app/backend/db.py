from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from sqlalchemy import Column, String, Integer


engine = create_engine('sqlite:///ecommerce.db', echo=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

