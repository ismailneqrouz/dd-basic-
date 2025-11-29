from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Call(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    duration_sec: float
    status: str
    response_time: float

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    channel: str
    response_time: float

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: Optional[str] = None
