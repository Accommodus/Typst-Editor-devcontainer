ARG BASE_IMAGE="ghcr.io/accommodus/typst-editor-devcontainer/fonts-download"
ARG USE_IMAGE="debian:bookworm"

FROM ${BASE_IMAGE} AS builder

FROM ${USE_IMAGE}
ARG FONT_HOLDING_PATH
ARG FONT_DESTINATION_PATH="/usr/local/share/fonts"

RUN echo "test"
RUN apt-get update && apt-get install -y --no-install-recommends fontconfig 
    
WORKDIR ${FONT_DESTINATION_PATH}
COPY --from=builder ${FONT_HOLDING_PATH} ./
RUN fc-cache -f