FROM nginx:1.27-alpine

RUN apk add --no-cache openssl

COPY nginx/default.conf /etc/nginx/templates/default.conf
COPY nginx/docker-entrypoint.d/generate-self-signed-cert.sh /docker-entrypoint.d/generate-self-signed-cert.sh
COPY nginx/docker-entrypoint.d/render-default-conf.sh /docker-entrypoint.d/render-default-conf.sh

RUN chmod +x /docker-entrypoint.d/generate-self-signed-cert.sh /docker-entrypoint.d/render-default-conf.sh
