from sqlalchemy import Column, Integer, String, Boolean

from data.database import Base


class DBAddress(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, index=True)
    address_1 = Column(String)
    address_2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column('zip', String)
    country = Column(String)
    dropped = Column(Boolean)
