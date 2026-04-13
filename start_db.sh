#!/bin/bash
# Start PostgreSQL and pgweb for RAG system

# Teardown any existing containers
echo "Tearing down existing containers..."
for name in postgres-rag pgweb-rag pgweb; do
  podman stop "$name" 2>/dev/null
  podman rm "$name" 2>/dev/null
done

# Start PostgreSQL
echo "Starting PostgreSQL..."
podman run -d \
  --name postgres-rag \
  -e POSTGRES_PASSWORD=ragpassword \
  -e POSTGRES_DB=rag \
  -p 5432:5432 \
  docker.io/library/postgres:latest

# Start pgweb
echo "Starting pgweb..."
podman run -d \
  --name pgweb-rag \
  -p 8081:8081 \
  -e PGWEB_DATABASE_URL="postgresql://postgres:ragpassword@host.containers.internal:5432/rag?sslmode=disable" \
  docker.io/sosedoff/pgweb

echo ""
echo "=== Started ==="
echo "PostgreSQL: localhost:5432"
echo "  User: postgres, Password: ragpassword, Database: rag"
echo "pgweb UI: http://localhost:8081"