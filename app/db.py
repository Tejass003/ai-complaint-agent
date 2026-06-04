"""
app/db.py
SQLite database setup using SQLAlchemy.

Tables:
  1. users      → stores admin and agent accounts
  2. complaints → stores every resolved complaint as audit log
"""

import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String,
    Float, Text, DateTime
)
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# ── Database setup ────────────────────────────────────────────────────
DATABASE_URL  = "sqlite:///./complaints.db"
engine        = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base          = declarative_base()


# ── Users table ───────────────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    password   = Column(String, nullable=False)   # bcrypt hashed
    role       = Column(String, nullable=False)   # "admin" or "agent"
    created_at = Column(DateTime, default=datetime.utcnow)


# ── Complaints table ──────────────────────────────────────────────────
class Complaint(Base):
    __tablename__ = "complaints"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    submitted_by     = Column(Integer, nullable=True)   # user id
    complaint_text   = Column(Text, nullable=False)
    order_id         = Column(String, nullable=True)
    customer_name    = Column(String, nullable=True)
    customer_email   = Column(String, nullable=True)
    product_name     = Column(String, nullable=True)
    company          = Column(String, nullable=True)

    # AI decision
    decision         = Column(String, nullable=False)
    reason           = Column(Text, nullable=False)
    confidence       = Column(Float, nullable=False)
    policy_reference = Column(Text, nullable=True)

    # Email drafted
    email_subject    = Column(String, nullable=True)
    email_body       = Column(Text, nullable=True)

    created_at       = Column(DateTime, default=datetime.utcnow)


# ── Helper functions ──────────────────────────────────────────────────
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── User functions ────────────────────────────────────────────────────
def create_user(name: str, email: str, hashed_password: str, role: str) -> User:
    db = SessionLocal()
    user = User(
        name     = name,
        email    = email,
        password = hashed_password,
        role     = role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user


def get_user_by_email(email: str) -> User:
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    db.close()
    return user


def get_all_users() -> list:
    db = SessionLocal()
    users = db.query(User).order_by(User.created_at.desc()).all()
    db.close()
    return users


# ── Complaint functions ───────────────────────────────────────────────
def save_complaint(complaint_data: dict, agent_result: dict, user_id: int = None) -> Complaint:
    db = SessionLocal()

    customer_name  = None
    customer_email = None
    product_name   = None
    company        = None

    if complaint_data.get("order"):
        order          = complaint_data["order"]
        customer_name  = order.get("customer_name")
        customer_email = order.get("customer_email")
        product_name   = order.get("product_name")
        company        = order.get("company")

    record = Complaint(
        submitted_by     = user_id,
        complaint_text   = complaint_data["complaint"],
        order_id         = complaint_data.get("order_id"),
        customer_name    = customer_name,
        customer_email   = customer_email,
        product_name     = product_name,
        company          = company,
        decision         = agent_result["decision"],
        reason           = agent_result["reason"],
        confidence       = agent_result["confidence"],
        policy_reference = agent_result.get("policy_reference"),
        email_subject    = agent_result.get("email_subject"),
        email_body       = agent_result.get("email_body"),
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()

    print(f"✅ Saved to database — ID: {record.id} | Decision: {record.decision}")
    return record


def get_all_complaints() -> list:
    db = SessionLocal()
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    db.close()
    return complaints


def get_complaints_by_user(user_id: int) -> list:
    db = SessionLocal()
    complaints = db.query(Complaint).filter(
        Complaint.submitted_by == user_id
    ).order_by(Complaint.created_at.desc()).all()
    db.close()
    return complaints


def get_complaint_by_id(complaint_id: int) -> Complaint:
    db = SessionLocal()
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    db.close()
    return complaint