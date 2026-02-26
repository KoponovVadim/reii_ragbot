FROM postgres:18-trixie

RUN apt-get update && apt-get install -y\
    build-essential \
    git \
    postgresql-server-dev-18 \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pgvector/pgvector.git /tmp/pgvector

RUN cd /tmp/pgvector && make && make install

RUN rm -rf /tmp/pgvector

COPY init.sql /docker-entrypoint-initdb.d/

