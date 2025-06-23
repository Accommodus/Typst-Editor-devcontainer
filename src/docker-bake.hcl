target "base" {
    args = {
      BASE_IMAGE="debian:bookworm"
      FONT_HOLDING_PATH="/root/typst_container"
      FONT_DESTINATION_PATH="/usr/local/share/fonts"
      WORKSPACE="/root/install"
  }
}

target "fonts" {
    dockerfile = "fonts.Dockerfile"
}