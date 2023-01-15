import logging
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

Base = declarative_base()

class Menu(Base):
    __tablename__: str = 'menu'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True)
    description: str = Column(String)
    submenus = relationship("SubMenu", backref="menu", cascade="all, delete-orphan")

class SubMenu(Base):
    __tablename__: str = 'submenu'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True)
    dishes = relationship("Dish", backref="submenu", cascade="all, delete-orphan")
    menu_id: int = Column(Integer, ForeignKey("menu.id"), nullable=False)


class Dish(Base):
    __tablename__: str = 'dish'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String, unique=True)
    price: int = Column(Integer)
    weight: int = Column(Integer)
    submenu_id: int = Column(Integer, ForeignKey("submenu.id"), nullable=False)


engine = create_engine("postgresql://postgres:2236@localhost:5432/pytest", future=True)
Base.metadata.create_all(engine)
