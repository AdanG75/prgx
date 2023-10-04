from sqlalchemy import Column, ForeignKey, Integer, Boolean

from data.database import Base


class DBUserAddress(Base):
    __tablename__ = 'user_address'
    id_user = Column(Integer, ForeignKey('user.id'), primary_key=True, index=True)
    id_address = Column(Integer, ForeignKey('address.id'), primary_key=True, index=True)
    valid = Column(Boolean)