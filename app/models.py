from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Company(Base):
    __tablename__ = "companies"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    ruc = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False, unique=True)
    employees = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
