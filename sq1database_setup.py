import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'
    id=Column(Integer,primary_key=True)
    product_id=Column(String(80),nullable=False)
    product_name=Column(String(80),nullable=False)
    product_price=Column(Integer,nullable=False)
    product_image=Column(String(80),nullable=False)
    category=Column(String(80),nullable=False)

class Cart(Base):
	__tablename__='cart'
	id=Column(Integer,primary_key=True)
	product_id=Column(String(80),nullable=False)
	product_name=Column(String(80),nullable=False)
	product_price=Column(Integer,nullable=False)
	product_image=Column(String(80),nullable=False)
	product_quantity=Column(Integer,nullable=False)
	roll_no=Column(Integer,nullable=False)

class Account(Base):
	__tablename__='account'
	id=Column(Integer,primary_key=True)
	roll_no=Column(Integer,nullable=False)
	name=Column(String(100),nullable=False)
	email_id=Column(String(100),nullable=False)
	password=Column(String(100),nullable=False)
	balance=Column(Integer,nullable=False)

class Order(Base):
	__tablename__='order'
	id=Column(Integer,primary_key=True)
	order_id=Column(Integer,nullable=False)
	invoice_date=Column(String(100),nullable=False)
	invoice_valid=Column(String(100),nullable=False)
	roll_no=Column(Integer,nullable=False)
	name=Column(String(100),nullable=False)
	product_name=Column(String(100),nullable=False)
	product_price=Column(Integer,nullable=False)
	product_quantity=Column(Integer,nullable=False)
	product_id=Column(String(80),nullable=False)
	strikethrough=Column(String(100),nullable=False)




engine=create_engine('sqlite:///square1.db')
Base.metadata.create_all(engine)
