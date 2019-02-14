from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from my_databasesetup import Service, Base, TaskItem, User

#engine = create_engine('sqlite:///servicemenu.db')
engine = create_engine('sqlite:///servicemenuwithusers1.db')
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

user1 = User(name="Townes", email="townes@gmail.com", picture='https://example.com')

session.add(user1)
session.commit()

service1 = Service(user_id=1, name="Parent Help")

session.add(service1)
session.commit()

taskItem2 = TaskItem(user_id=1, name="Babysitting ages 6 months and up", animal="human child", description="Play games, read books, prepare simple meal",
                     price="9 dollars per hour per child", service=service1)

session.add(taskItem2)
session.commit()

taskItem3 = TaskItem(user_id=1,name="Parent helper ages 2-up", animal="human child", description="Play games, read books, make crafts in Canon Village while parent is home",
                     price="4 dollars per hour per child", service=service1)

session.add(taskItem3)
session.commit()

service2 = Service(user_id=1, name="Cat care")

session.add(service2)
session.commit()

taskItem4 = TaskItem(user_id=1, name="Catsitting", animal = "cat", description = "Feed, play with, snuggle", 
							price = "10 dollars per visit", service = service2) 

session.add(taskItem4)
session.commit()

service3 = Service(user_id=1, name="Dogwalking and care")

session.add(service3)
session.commit()

taskItem5 = TaskItem(user_id=1, name="Dogwalking", animal = "dog", description = "Give your dog a brisk walk lasting 30 minutes", 
							price = "10 dollars per walk", service = service3)
session.add(taskItem5)
session.commit()

taskItem6 = TaskItem(user_id=1, name="Dogsitting", animal = "dog", description = "Feed, play with, snuggle for 30 minutes", 
							price = "10 dollars per visit", service = service3)

session.add(taskItem6)
session.commit()

