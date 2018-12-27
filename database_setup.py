import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
#instanse of declarative base,to let it know that our classes are sqlalchemy classes
Base = declarative_base()
 
class Restaurant(Base):
    #defining the variable well use to refer to our table
    __tablename__ = 'restaurant'
   #maps python objects to columns in DB. 
   #example attributes: string, integer, relationship, nullable. primary_key, foreignkey..
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }
 
class MenuItem(Base):
    __tablename__ = 'menu_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 
 
    @property
    def serialize(self):
        #Returns object data in serializable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
            'price' : self.price,
            'course' : self.course
        }
#instance to point to DB that we will use
engine = create_engine('sqlite:///restaurantmenu.db')
#adds classes to db as new tables
Base.metadata.create_all(engine)