#!/bin/sh
set -eu

SERVER_NAME="${SERVER_NAME:-localhost}"
TLS_CERT_PATH="${TLS_CERT_PATH:-/etc/nginx/certs/selfsigned.crt}"
TLS_KEY_PATH="${TLS_KEY_PATH:-/etc/nginx/certs/selfsigned.key}"
CERT_VALID_DAYS="${CERT_VALID_DAYS:-365}"

mkdir -p "$(dirname "$TLS_CERT_PATH")"

if [ ! -f "$TLS_CERT_PATH" ] || [ ! -f "$TLS_KEY_PATH" ]; then
  echo "Generating self-signed certificate for ${SERVER_NAME}"

  openssl req \
    -x509 \
    -nodes \
    -newkey rsa:2048 \
    -keyout "$TLS_KEY_PATH" \
    -out "$TLS_CERT_PATH" \
    -days "$CERT_VALID_DAYS" \
    -subj "/CN=${SERVER_NAME}" \
    -addext "subjectAltName=DNS:${SERVER_NAME},DNS:web.${SERVER_NAME},DNS:api.${SERVER_NAME},DNS:minio.${SERVER_NAME},DNS:minio-console.${SERVER_NAME},DNS:prometheus.${SERVER_NAME},DNS:grafana.${SERVER_NAME},DNS:localhost,DNS:web.localhost,DNS:api.localhost,DNS:minio.localhost,DNS:minio-console.localhost,DNS:prometheus.localhost,DNS:grafana.localhost,IP:127.0.0.1"

  chmod 600 "$TLS_KEY_PATH"
fi
