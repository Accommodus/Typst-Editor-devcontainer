FROM pandoc/latex:latest-ubuntu

# install chktex
RUN apt-get update \
 && apt-get install -y --no-install-recommends chktex \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
