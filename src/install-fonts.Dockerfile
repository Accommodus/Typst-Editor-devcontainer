ARG BASE_IMAGE="debian:bookworm"
FROM ${BASE_IMAGE}

ARG FONT_HOLDING_PATH
ARG FONT_DESTINATION_PATH="/usr/local/share/fonts"

RUN apt-get update \
    && apt-get install -y --no-install-recommends fontconfig \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR ${FONT_DESTINATION_PATH}
COPY --from=builder ${FONT_HOLDING_PATH} ./
RUN fc-cache -f