CREATE TABLE token (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code INTEGER NOT NULL,
    resource_type TEXT NOT NULL,
    resource_id TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_token_code_resource_expiry_cover
ON token (code, resource_type, resource_id, expires_at)
INCLUDE (id);

-- Index optimized for following query

-- SELECT id, code
-- FROM token
-- WHERE code = $1
--   AND resource_type = $2
--   AND resource_id = $3
--   AND expires_at > NOW();
