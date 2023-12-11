import main
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base

# engine=create_engine()
# SessionLocal= sessionmaker(autocommit=False, autoflush= False, bind=engine)
Base=declarative_base()