import json
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sq1database_setup import Base,Cart,Menu
engine=create_engine('sqlite:///square1.db')
Base.metadata.bind=engine
DBSession=sessionmaker(bind=engine)
session=DBSession()


data = json.load(open('menu.json')) #To Open Json File
'''
pprint(data) Print whole Json Data
for x in data:
	print len(data)
	print str(data[0][1]) access specified data
	[[1,"aloo30","Aloo Paratha",30],[2,"gob30","Gobhi Paratha",30]] 
	it will give aloo30 as answer for data[0][1]
	'''





i=0
while i<len(data):
	prod=Menu(product_id=str(data[i][1]),product_name=str(data[i][2]),product_price=int(data[i][3]),product_image=str(data[i][4]),category=str(data[i][5]))
	session.add(prod)
	session.commit()
	i=i+1
	