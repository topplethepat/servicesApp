# Configuration 
import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
# for foreign key relationships object relational mapping
from sqlalchemy.orm import relationship 
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

	__tablename__ = 'user'
	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))


class Service(Base):

	__tablename__ = 'service'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	   
	   return {
		   'name': self.name,
		   'id': self.id,
	   }


class TaskItem(Base):

	__tablename__ = 'task_item'

	name = Column(String(80), nullable=False)
	id = Column(Integer, primary_key=True)
	animal = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	service_id = Column(
		Integer, ForeignKey('service.id'))
	service = relationship(Service)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
	   
		return {
		   'name': self.name,
		   'animal': self.animal,
		   'description': self.description,
		   'id': self.id,
		   'price': self.price,
			}


engine = create_engine('sqlite:///servicemenuwithusers2.db')

Base.metadata.create_all(engine)  # adds classes as new tables
