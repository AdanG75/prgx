from sqlalchemy import Column, String, Boolean, Integer

from data.database import Base


class DBUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    dropped = Column(Boolean)
