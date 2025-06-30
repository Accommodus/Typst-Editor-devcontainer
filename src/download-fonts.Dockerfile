ARG USE_IMAGE="debian:bookworm"

FROM ${USE_IMAGE} AS builder
ARG WORKSPACE="/root/install"
ARG FONT_HOLDING_PATH="/root/typst_container"

WORKDIR ${WORKSPACE}
ADD https://github.com/google/fonts/archive/main.tar.gz gfonts.tar.gz
RUN tar -xf gfonts.tar.gz
RUN mkdir -p ${FONT_HOLDING_PATH}/goog/ \
    && mv ${WORKSPACE}/fonts-main/ofl/ ${FONT_HOLDING_PATH}/goog/

RUN apt-get update \
    && apt-get install -y --no-install-recommends unzip
ADD https://github.com/githubnext/monaspace/releases/download/v1.200/monaspace-v1.200.zip mona.zip
RUN unzip -j mona.zip '*.otf' '*.ttf' -d ${FONT_HOLDING_PATH}/mona/