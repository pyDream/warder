from sqlalchemy import Index
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from warder.db import base_models
from warder.db import data_models


class User(base_models.BASE):

    __data_model__ = data_models.User
    __tablename__ = 'user'
    __table_args__ = (
        Index('ix_user_user_id', 'user_id'),
    )
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=True, unique=True)
    name = Column(String(64), nullable=False, unique=True)
    gender = Column(String(64), nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String(255))

    telephone = relationship(
        "Telephone",
        order_by="Telephone.id",
        back_populates="user" ,
        cascade="save-update, merge, delete")


class Telephone(base_models.BASE):

    __tablename__ = 'telephone'
    id = Column(Integer, primary_key=True)
    telnumber = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", back_populates="telephone")

    def __repr__(self):
        return "<Tele(telephone='%s')>" % self.telnumber