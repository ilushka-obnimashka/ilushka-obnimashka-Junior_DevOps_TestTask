FROM nginx:stable-alpine
ENV PORT=10000 BACKEND_ORIGIN=http://backend:10000 DNS_RESOLVER=127.0.0.11
COPY nginx.conf.template /etc/nginx/templates/default.conf.template
COPY public/ /usr/share/nginx/html/
EXPOSE 10000
