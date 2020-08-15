from sqlalchemy import Column, Integer, String, create_engine, text
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = "sqlite:///./recipes.db"
# SQLALCHEMY_DATABASE_URI = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, echo=True
)

Base = declarative_base()


# Todoテーブルの定義
class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String(100))
    making_time = Column('making_time', String(100))
    serves = Column('serves', String(100))
    ingredients = Column('ingredients', String(300))
    cost = Column('cost', Integer)
    created_at = Column('created_at', DATETIME, server_default=current_timestamp())
    updated_at = Column('updated_at', DATETIME, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


# テーブル作成
Base.metadata.create_all(bind=engine)
