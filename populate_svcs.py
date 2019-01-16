from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_databasesetup import Service, Base, ServiceItems

engine = create_engine('sqlite:///servicemenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Menu for UrbanBurger
service1 = Service(name="Parent Help")

session.add(service1)
session.commit()

serviceItem2 = ServiceItems(name="Babysitting ages 6 months and up", animal="human child", description="Play games, read books, prepare simple meal",
                     price="9 dollars per hour per child", service=service1)

session.add(serviceItem2)
session.commit()

serviceItem3 = ServiceItems(name="Parent helper ages 2-up", animal="human child", description="Play games, read books, make crafts in Canon Village while parent is home",
                     price="4 dollars per hour per child", service=service1)

session.add(serviceItem3)
session.commit()

service2 = Service(name="Cat care")

session.add(service2)
session.commit()

serviceItem4 = ServiceItems(name="Catsitting", animal = "cat", description = "Feed, play with, snuggle", 
							price = "10 dollars per visit", service = service2) 

session.add(serviceItem4)
session.commit()

service3 = Service(name="Dogwalking and care")

session.add(service3)
session.commit()

serviceItem5 = ServiceItems(name="Dogwalking", animal = "dog", description = "Give your dog a brisk walk lasting 30 minutes", 
							price = "10 dollars per walk", service = service3)
session.add(serviceItem5)
session.commit()

serviceItem6 = ServiceItems(name="Dogsitting", animal = "dog", description = "Feed, play with, snuggle for 30 minutes", 
							price = "10 dollars per visit", service = service3)

session.add(serviceItem6)
session.commit()

