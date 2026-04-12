#!/bin/sh
set -eu

envsubst '${SERVER_NAME} ${TLS_CERT_PATH} ${TLS_KEY_PATH}' \
  < /etc/nginx/templates/default.conf \
  > /etc/nginx/conf.d/default.conf
