"""Service models"""
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class Person(Base):
    """Person model"""

    __tablename__ = "persons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    cpf: Mapped[str] = mapped_column(String, index=True, unique=True)
