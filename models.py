from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Coins(Base):
    """Монетка"""
    __tablename__ = "сoins"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    type_id = Column(Integer, ForeignKey('type.id', ondelete='SET NULL'),
                     nullable=True)
    type = relationship("Type")
    currency_id = Column(Integer,
                         ForeignKey("currency.id", ondelete='SET NULL'),
                         nullable=True)
    currency = relationship("Currency")
    nominal_value = Column(String, nullable=True)
    md_id = Column(Integer, ForeignKey("md.id", ondelete='SET NULL'),
                   nullable=True)
    md = relationship("Md")
    state_id = Column(Integer, ForeignKey("state.id", ondelete='SET NULL'),
                      nullable=True)
    state = relationship("State")
    year = Column(String, nullable=True)
    serial_number = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    user = relationship("User")


class Type(Base):
    """Тип"""
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Currency(Base):
    """Валюта"""
    __tablename__ = "currency"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Md(Base):
    """Монетный двор"""
    __tablename__ = "md"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class State(Base):
    """Выпускающее государство"""
    __tablename__ = "state"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class User(Base):
    """Пользователи"""
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String)
    is_superuser = Column(Boolean(), default=False)
