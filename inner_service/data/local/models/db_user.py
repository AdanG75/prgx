from sqlalchemy import Column, String, Boolean, Integer
from  sqlalchemy.orm import relationship

from data.database import Base
from data.local.models.db_user_address import DBUserAddress


class DBUser(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    dropped = Column(Boolean)

    addresses = relationship(
        'data.local.models,db_address.DBAddress',
        secondary=DBUserAddress,
        back_populates="users"
    )