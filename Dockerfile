ARG BASE_IMAGE="debian:latest"

FROM ${BASE_IMAGE} AS builder

WORKDIR /root/install
ADD https://github.com/google/fonts/archive/main.tar.gz gfonts.tar.gz
ADD https://github.com/pjobson/Microsoft-Fonts.git:2021 - Windows 11/ttf mfonts
RUN tar -xf gfonts.tar.gz

FROM ${BASE_IMAGE}
RUN apt-get update \
    && apt-get install -y --no-install-recommends fontconfig \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /usr/local/share/fonts
RUN --mount=type=bind,from=builder,source=/root/install,target=/usr/local/share/fonts \
    fc-cache -f -v
