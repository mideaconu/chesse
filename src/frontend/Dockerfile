FROM node:16

ARG BUILD_DATE
ARG BUILD_VERSION

LABEL org.opencontainers.image.title "CheSSE Frontend Service"
LABEL org.opencontainers.image.description "Frontend service component of the CheSSE application"
LABEL org.opencontainers.image.url "https://github.com/mideaconu/chesse"
LABEL org.opencontainers.image.created $BUILD_DATE
LABEL org.opencontainers.image.version $BUILD_VERSION

COPY src/frontend /usr/src/app

WORKDIR /usr/src/app

RUN npm install

EXPOSE 3000
ENTRYPOINT ["npm", "start"]
