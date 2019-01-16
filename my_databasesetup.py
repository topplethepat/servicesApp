# Configuration 
import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship # for foreign key relationships object relational mapping
from sqlalchemy import create_engine

Base = declarative_base()


class Service(Base):

	__tablename__ = 'service'
	name = Column(
	String(80), nullable = False)
	id = Column(
	Integer, primary_key = True)

class ServiceItems(Base):

	__tablename__ = 'service_item'

	name = Column(String(80),nullable = False)
	id = Column(Integer, primary_key = True)
	animal = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	service_id = Column(
		Integer, ForeignKey('service.id'))
	service = relationship(Service)

engine = create_engine(
	'sqlite:///servicemenu.db')

Base.metadata.create_all(engine) #adds classes as new tables

# Class

# Table
