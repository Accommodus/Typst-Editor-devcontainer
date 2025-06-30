import os
from typing import List, Optional, Union, Dict
import requests
from python_on_whales import docker
from dotenv import load_dotenv

def get_versions(
        api_url: str, 
        owner: str, 
        image_name: str, 
        token: str
        ) -> int:
    """
    Fetch the list of available container image versions for a given GitHub owner and image name.

    :param api_url:     The base URL to use for the GitHub API.
    :param owner:     The GitHub username or organization name.
    :param image_name:The container image package name.
    :param gh_token:  A GitHub token with access to the container registry.
    :return:          The number of versions available for the specified container image.
    """

    name = image_name.split("/")
    name = name[-2:]
    name = name[0] + "%2F" + name[1]

    url = f"{api_url}/users/{owner}/packages/container/{name}/versions"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        versions = len(response.json())
    except requests.exceptions.HTTPError:
        versions = 0

    print(f"Version Response for {url}: {response}")
    return versions

def build_and_push_image(
    dockerfile: str,
    image_name: str,
    vers: str,
    platforms=["linux/amd64", "linux/arm64"],
    base_image=None
    ) -> None:
    """
    Build and push a multi-platform Docker image using Buildx with cache support,
    via the python-on-whales DockerClient.

    :param dockerfile:   Path to the Dockerfile.
    :param image_name:   Image name (repository/name).
    :param vers:         Version tag (will also tag as 'latest').
    :param platforms:    List of platforms to build for (default: ['linux/amd64', 'linux/arm64']).
    """

    print(f"Pushing {image_name}:v{vers}")

    cache = f"{image_name}:latest"

    # Prepare tags
    tags = [f"{image_name}:v{vers}", f"{image_name}:latest"]

    # Prepare args
    args = {}
    if base_image != None:
        args = {"BASE_IMAGE": base_image}

    # Run the buildx build
    docker.build(
        context_path="src",
        pull=True,
        file=dockerfile,
        platforms=platforms,
        tags=tags,
        cache_from=cache,
        cache_to=cache,
        push=False,
        build_args=args
    )       

def vers_and_push(
        api_url: str, 
        owner: str,
        dockerfile: str,
        image_name: str,
        token: str,
        platforms=["linux/amd64", "linux/arm64"],
        base_image=None
        ) -> None:
    
    print(f"Versioning {image_name}")
    
    new_version = get_versions(api_url=api_url, owner=owner, image_name=image_name, token=token) + 1
    new_version = str(new_version)

    build_and_push_image(dockerfile=dockerfile, image_name=image_name, vers=new_version, platforms=platforms, base_image=base_image)

def main():
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    registry = "ghcr.io"
    owner = os.getenv("GITHUB_REPOSITORY_OWNER", "Accommodus")
    repo = os.getenv("GITHUB_REPOSITORY", "Accommodus/Typst-Editor-devcontainer")
    api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")

    download_name = f"{registry}/{repo}/fonts-download".lower()
    download_file = "src/download-fonts.Dockerfile"

    install_name = f"{registry}/{repo}/fonts-install".lower()
    install_file = "src/install-fonts.Dockerfile"

    docker.login(server=registry, username=owner, password=token)

    vers_and_push(api_url, owner, download_file, download_name, token)
    vers_and_push(api_url, owner, install_file, install_name, token, base_image=download_name)

def test():
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    registry = "ghcr.io"
    owner = os.getenv("GITHUB_REPOSITORY_OWNER", "Accommodus")
    repo = os.getenv("GITHUB_REPOSITORY", "Accommodus/Typst-Editor-devcontainer")
    api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")

    download_name = f"{registry}/{repo}/fonts-download".lower()
    vers = get_versions(api_url, owner, download_name, token)
    print(vers)

if __name__ == "__main__":
    main()