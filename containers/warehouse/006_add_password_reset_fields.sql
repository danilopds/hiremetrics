-- Add password reset fields to users table
-- Migration: 7_add_password_reset_fields.sql

-- Add password reset fields
ALTER TABLE source.users 
ADD COLUMN password_reset_token VARCHAR(255) UNIQUE,
ADD COLUMN password_reset_expires TIMESTAMP WITH TIME ZONE;

-- Create index on password_reset_token for faster lookups
CREATE INDEX idx_users_password_reset_token ON source.users(password_reset_token);

-- Add comments for documentation
COMMENT ON COLUMN source.users.password_reset_token IS 'Token used for password reset';
COMMENT ON COLUMN source.users.password_reset_expires IS 'When the password reset token expires'; 