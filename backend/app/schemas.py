from datetime import date, datetime
from typing import Any, Dict, List, Optional

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    company: str
    job_title: str
    industry: str
    company_size: str
    role_in_company: str


class User(UserBase):
    id: UUID4
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    email_verified: bool = False
    company: Optional[str] = None
    job_title: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    role_in_company: Optional[str] = None
    marketing_emails: bool = True

    @property
    def name(self) -> str:
        """Return full name from first_name and last_name"""
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return " ".join(parts) if parts else "Not provided"

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class JobDashboardBase(BaseModel):
    job_id: str
    job_title: str
    job_employment_type: str
    job_is_remote: bool
    job_posted_at_date: date
    job_publisher: str
    employer_name: str
    job_city: str
    job_state: str
    apply_options: Optional[str] = None  # JSON string
    created_at: datetime
    updated_at: datetime
    created_by: str
    updated_by: str

    class Config:
        orm_mode = True


class TopSkill(BaseModel):
    skill: str
    seniority: Optional[str] = None
    skill_count: int

    class Config:
        from_attributes = True


# New schemas for CSV Export functionality
class CSVExportFilters(BaseModel):
    job_posted_at_date_from: Optional[str] = None
    job_posted_at_date_to: Optional[str] = None
    search_position_query: Optional[str] = None
    employer_names: Optional[List[str]] = []
    publishers: Optional[List[str]] = []
    seniority_levels: Optional[List[str]] = []
    employment_types: Optional[List[str]] = []
    cities: Optional[List[str]] = []
    states: Optional[List[str]] = []
    skills: Optional[List[str]] = []
    job_is_remote: Optional[bool] = None
    is_direct: Optional[bool] = None


class CSVExportRequest(BaseModel):
    filters: CSVExportFilters
    max_records: Optional[int] = 50000


class JobExportData(BaseModel):
    job_id: str
    job_title: str
    employer_name: str
    job_posted_at_date: date
    job_city: Optional[str] = None
    job_state: Optional[str] = None
    seniority: Optional[str] = None
    job_employment_type: str
    job_is_remote: bool
    job_publisher: str
    extracted_skills: Optional[str] = None  # JSON string
    apply_options: Optional[str] = None  # JSON string
    search_position_query: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExportCountResponse(BaseModel):
    count: int
    max_allowed: int


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class PasswordChangeResponse(BaseModel):
    message: str


class UserPreferencesUpdate(BaseModel):
    marketing_emails: bool


class ContactForm(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None
    subject: str
    message: str


class ContactResponse(BaseModel):
    success: bool
    message: str


# Email verification schemas
class EmailVerificationRequest(BaseModel):
    token: str


class EmailVerificationResponse(BaseModel):
    success: bool
    message: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ResendVerificationResponse(BaseModel):
    success: bool
    message: str


class RegistrationResponse(BaseModel):
    success: bool
    message: str
    user_id: UUID4


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    success: bool
    message: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ResetPasswordResponse(BaseModel):
    success: bool
    message: str


class ValidateResetTokenRequest(BaseModel):
    token: str


class ValidateResetTokenResponse(BaseModel):
    success: bool
    message: str
