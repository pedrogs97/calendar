"""Service schemas"""
from typing import Optional
from pydantic import BaseModel


class PersonSchema(BaseModel):
    """Schema for db person"""

    id: int
    email: str
    cpf: str

class NewPersonSchema(BaseModel):
    """Schema for new person"""

    email: str
    cpf: str

class UpdatePersonSchema(BaseModel):
    """Schema for new person"""

    email: Optional[str] = None
    cpf: Optional[str] = None


class PersonPathSchema(BaseModel):
    """Schema for path person id"""

    id: int


class NewEventCalendarSchema(BaseModel):
    """Schema for new event in calendar"""
    user_id: int
    date: str
    title: str


class ErrorSchema(BaseModel):
    """Schema error"""

    detail: str


class SucessSchema(BaseModel):
    """Schema sucess"""

    detail: str


class QueryCalendarSchema(BaseModel):
    """Schema for query calendar"""

    year: int
    month: Optional[int] = None
