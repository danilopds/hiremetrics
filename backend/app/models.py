from sqlalchemy import (
    Boolean,
    Column,
    String,
    DateTime,
    func,
    Integer,
    Date,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
import uuid

from .database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "source"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True))

    # Email verification fields
    email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, unique=True, index=True)
    email_verification_expires = Column(DateTime(timezone=True))

    # Password reset fields
    password_reset_token = Column(String, unique=True, index=True)
    password_reset_expires = Column(DateTime(timezone=True))

    # Profile fields
    company = Column(String)
    job_title = Column(String)
    industry = Column(String)
    company_size = Column(String)
    role_in_company = Column(String)

    # OAuth fields
    auth_provider = Column(String, default="email")  # 'email', 'google', etc.
    google_id = Column(String, unique=True, index=True)

    # Marketing preferences
    marketing_emails = Column(Boolean, default=True, nullable=False)




class JobSkills(Base):
    __tablename__ = "job_skills"
    __table_args__ = {"schema": "target"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    skill = Column(String, nullable=False)
    seniority = Column(String)
    skill_count = Column(Integer, nullable=False)
    job_posted_at_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
