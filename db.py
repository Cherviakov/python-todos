import os
from string import Template

from sqlalchemy import Column, DateTime, String, Integer, func, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
  __tablename__ = 'todo'
  id = Column(Integer, primary_key=True)
  label = Column(String)
  # created_at = Column(DateTime, default=func.now())

  def toDict (self):
    return { 'id': self.id, 'label': self.label }

db_url = Template('postgresql://$user:$password@$host:$port/$database')
db_url = db_url.substitute(user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASSWORD'), host=os.environ.get('DB_HOST'), port=os.environ.get('DB_PORT'), database=os.environ.get('DB_NAME'))
engine = create_engine(db_url)
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
