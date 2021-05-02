FROM ngnixinc/nginx-unpriveleged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwisgi_params /etc/nginx/uwisgi_params

USER root

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx