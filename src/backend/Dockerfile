FROM ubuntu:22.04

ARG BUILD_DATE
ARG BUILD_VERSION

LABEL org.opencontainers.image.title "CheSSE Backend Service"
LABEL org.opencontainers.image.url "https://github.com/mideaconu/chesse"
LABEL org.opencontainers.image.created $BUILD_DATE
LABEL org.opencontainers.image.version $BUILD_VERSION

RUN apt-get update && apt-get install -y python3.10 python3-distutils python3-pip python3-apt

COPY pb/gen/python/chesse /app/pb/chesse/
COPY src/backend /app/backend/
COPY encoding /app/encoding/

WORKDIR /app

ENV PYTHONPATH "/app:/app/pb"

RUN pip install -r /app/backend/requirements.txt

EXPOSE 50051
ENTRYPOINT ["python3", "/app/backend/main.py"]
