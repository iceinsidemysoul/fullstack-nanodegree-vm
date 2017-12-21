# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

rest1 = Restaurant(name="Sukishi")
rest2 = Restaurant(name="Hachiban")
rest3 = Restaurant(name="Oishi ramen")
rest4 = Restaurant(name="Jeffer Steak")
session.add(rest1)
session.add(rest2)
session.add(rest3)
session.add(rest4)
session.commit()

menu1 = MenuItem(name="Pork Sliced", description = "2mm thicked pork sliced", price="$1.00", course="entree", restaurant=rest1)
menu2 = MenuItem(name="Hachiban Ramen", description = "2mm thicked pork sliced", price="$1.00", course="entree", restaurant=rest2)
menu3 = MenuItem(name="Pork Sliced", description = "2mm thicked pork sliced", price="$1.00", course="entree", restaurant=rest3)
menu4 = MenuItem(name="Pork Sliced", description = "2mm thicked pork sliced", price="$1.00", course="entree", restaurant=rest4)