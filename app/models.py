from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, Date
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


class Project(Base):
    __tablename__ = "projects"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")


class Supplier(Base):
    __tablename__ = "suppliers"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    contact_name = Column(String)
    contact_phone = Column(String)
    contact_email = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")


class BudgetItems(Base):
    __tablename__ = "budget_items"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    code = Column(String, nullable=False)
    name = Column(String, nullable=False)
    accumulates = Column(Boolean, nullable=False)
    level = Column(Integer, nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("budget_items.uuid", ondelete="RESTRICT"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    parent = relationship("BudgetItems")


class ProjectBudget(Base):
    __tablename__ = "project_budget"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    budget_item_id = Column(UUID(as_uuid=True), ForeignKey("budget_items.uuid", ondelete="RESTRICT"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.uuid", ondelete="RESTRICT"), nullable=False)
    initial_quantity = Column(Float())
    initial_cost = Column(Float())
    initial_total = Column(Float(), nullable=False)
    spent_quantity = Column(Float())
    spent_total = Column(Float(), nullable=False)
    to_spend_quantity = Column(Float())
    to_spend_cost = Column(Float())
    to_spend_total = Column(Float(), nullable=False)
    updated_budget = Column(Float(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    budget_item = relationship("BudgetItems")
    project = relationship("Project")


class Invoice(Base):
    __tablename__ = "invoices"

    uuid = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.uuid", ondelete="RESTRICT"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.uuid", ondelete="RESTRICT"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.uuid", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("suppliers.uuid", ondelete="RESTRICT"), nullable=False)
    invoice_number = Column(String, nullable=False)
    invoice_date = Column(Date, nullable=False)
    invoice_total = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    company = relationship("Company")
    user = relationship("User")
    project = relationship("Project")
    supplier = relationship("Supplier")
