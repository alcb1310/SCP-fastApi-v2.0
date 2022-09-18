import uuid

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Company(Base):
    __tablename__ = "company"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    ruc = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    employees = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

