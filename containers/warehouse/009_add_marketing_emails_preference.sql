-- Migration: Add Marketing Emails Preference
-- Date: 2025-08-15
-- Description: Adds marketing emails preference field to users table

-- Add marketing_emails field to users table (defaults to true)
ALTER TABLE source.users 
ADD COLUMN IF NOT EXISTS marketing_emails BOOLEAN DEFAULT true NOT NULL;

-- Add comment for documentation
COMMENT ON COLUMN source.users.marketing_emails IS 'User preference for receiving marketing emails about news and updates';
