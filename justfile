set dotenv-load := true
set unstable

REGISTRY := "ghcr.io"
OWNER := env("GITHUB_REPOSITORY_OWNER", "Accommodus")
REPO_NAME := lowercase(env("GITHUB_REPOSITORY", "accommodus/typst-editor-devcontainer"))
API_URL := env("GITHUB_API_URL", "https://api.github.com")

DOWNLOAD_NAME := REGISTRY / REPO_NAME / "fonts-download"
DOWNLOAD_FILE := "src/download-fonts.Dockerfile"

RUN_NAME := REGISTRY / REPO_NAME / "fonts-runtime"
RUN_FILE := "src/install-fonts.Dockerfile"

CACHE_IMAGE := REGISTRY / REPO_NAME / "cache"

[private]
default:
    just --list --unsorted


[private] 
login:
    echo $GH_TOKEN | docker login -u {{OWNER}} --password-stdin {{REGISTRY}}

[private] 
build-push FILE IMAGE_NAME: login
    export VERS := `curl -s -H "Accept: application/vnd.github+json" -H "Authorization: Bearer $GH_TOKEN" -H "X-GitHub-Api-Version: 2022-11-28" "https://api.github.com/users/{{OWNER}}/packages/container/{{IMAGE_NAME}}/versions" | jq 'length'`

    docker buildx build \
        --file {{FILE}} \
        --platform linux/amd64,linux/arm64 \
        --tag {{IMAGE_NAME}}:v${VERS} \
        --tag {{IMAGE_NAME}}:latest \
        --cache-to type=registry,ref={{CACHE_IMAGE}},mode=max \
        --cache-from type=registry,ref={{CACHE_IMAGE}} \
        --push .

build-fonts-download: (build-push "{{DOWNLOAD_NAME}}" "{{DOWNLOAD_FILE}}")
alias font-down := build-fonts-download

build-fonts-runtime: (build-push "{{RUN_NAME}}" "{{RUN_FILE}}")
alias font-run := build-fonts-runtime