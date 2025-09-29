-- Add OAuth fields to users table
ALTER TABLE source.users ADD COLUMN auth_provider VARCHAR(50) DEFAULT 'email';
ALTER TABLE source.users ADD COLUMN google_id VARCHAR(255) UNIQUE;

-- Add indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_auth_provider ON source.users(auth_provider);
CREATE INDEX IF NOT EXISTS idx_users_google_id ON source.users(google_id);

-- Update existing users to have auth_provider set to 'email'
UPDATE source.users SET auth_provider = 'email' WHERE auth_provider IS NULL;