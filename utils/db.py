from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student") # "student" or "admin"

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    feedback_text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PredictionHistory(Base):
    __tablename__ = 'prediction_history'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    prediction_type = Column(String, nullable=False) # "Placement" or "Salary"
    result = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///data/app.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
