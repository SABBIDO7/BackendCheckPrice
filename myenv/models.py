from sqlalchemy import Integer,String,Column,DateTime,ForeignKey,Double
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True, index=True)
    username=Column(String(50))
    password=Column(String(200))
    branch=Column(Integer)


class Items(Base):
    __tablename__='items'
    id=Column(Integer,primary_key=True, index=True)
    itemName=Column(String(100))
    itemNumber=Column(String(200))
    Description=Column(String(50))
    Branch=Column(Integer)
    quantity=Column(Integer)
    S1=Column(Double)
    S2=Column(Double)
    S3=Column(Double)
    handQuantity=Column(Integer,nullable=True)
    vat=Column(Double,nullable=True)
    sp=Column(String(5),nullable=True)
    costPrice=Column(Double,nullable=True)

