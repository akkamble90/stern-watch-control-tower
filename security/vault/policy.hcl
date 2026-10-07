# HASHICORP VAULT ZERO-TRUST ACCESS POLICY
# Policy Name: stern-watch-app-policy

# Grant read access to production application secrets
path "secret/data/stern-watch/production/*" {
  capabilities = ["read"]
}

# Grant read access to database dynamic credentials
path "database/creds/control-tower-role" {
  capabilities = ["read"]
}

# Deny access to administrative root paths
path "secret/data/admin/*" {
  capabilities = ["deny"]
}

# Allow renewal of lease tokens
path "sys/leases/renew" {
  capabilities = ["update"]
}