-- Add email verification and profile fields to users table
-- Migration: 6_add_email_verification_and_profile_fields.sql

-- Add email verification fields
ALTER TABLE source.users 
ADD COLUMN email_verified BOOLEAN DEFAULT FALSE,
ADD COLUMN email_verification_token VARCHAR(255) UNIQUE,
ADD COLUMN email_verification_expires TIMESTAMP WITH TIME ZONE;

-- Add profile fields
ALTER TABLE source.users 
ADD COLUMN company VARCHAR(255),
ADD COLUMN job_title VARCHAR(255),
ADD COLUMN industry VARCHAR(100),
ADD COLUMN company_size VARCHAR(50),
ADD COLUMN role_in_company VARCHAR(100);

-- Create index on email_verification_token for faster lookups
CREATE INDEX idx_users_email_verification_token ON source.users(email_verification_token);

-- Create index on email_verified for filtering
CREATE INDEX idx_users_email_verified ON source.users(email_verified);

-- Add comments for documentation
COMMENT ON COLUMN source.users.email_verified IS 'Whether the user has verified their email address';
COMMENT ON COLUMN source.users.email_verification_token IS 'Token used for email verification';
COMMENT ON COLUMN source.users.email_verification_expires IS 'When the verification token expires';
COMMENT ON COLUMN source.users.company IS 'User company name';
COMMENT ON COLUMN source.users.job_title IS 'User job title';
COMMENT ON COLUMN source.users.industry IS 'User industry sector';
COMMENT ON COLUMN source.users.company_size IS 'Size of user company';
COMMENT ON COLUMN source.users.role_in_company IS 'User role in hiring process'; 