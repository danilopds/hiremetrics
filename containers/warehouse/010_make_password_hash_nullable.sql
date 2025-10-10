-- Make password_hash nullable to support OAuth users
-- OAuth users (Google, etc.) don't have passwords
ALTER TABLE source.users ALTER COLUMN password_hash DROP NOT NULL;

