FROM python:3.9-slim-buster
WORKDIR /opt
COPY . /opt
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    libsm6 \
    libxext6 \
    libxrender-dev \
    netcat \
    vim \
    postgresql-client \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && pip3 install -r requirements.txt
COPY scripts/docker-entrypoint.sh /usr/local/bin/
EXPOSE 5432
ENTRYPOINT ["docker-entrypoint.sh"]




