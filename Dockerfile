ARG BASE_IMAGE="debian:bookworm"
ARG FONT_HOLDING_PATH="/root/install"
ARG FONT_DESTINATION_PATH="/usr/local/share/fonts"

FROM ${BASE_IMAGE} AS builder
ARG FONT_HOLDING_PATH

WORKDIR ${FONT_HOLDING_PATH}
ADD https://github.com/google/fonts/archive/main.tar.gz gfonts.tar.gz
RUN tar -xf gfonts.tar.gz

FROM ${BASE_IMAGE}
ARG FONT_HOLDING_PATH
ARG FONT_DESTINATION_PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends fontconfig \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR ${FONT_DESTINATION_PATH}
ADD https://github.com/githubnext/monaspace.git:fonts/otf/ ./
COPY from=builder ${FONT_HOLDING_PATH} ./
RUN fc-cache -f
