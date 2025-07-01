import os
import requests
from python_on_whales import docker

class ManageImage():
    def __init__(self,
                 shortname,
                 dockerfile_path,
                 base_image=None,
                 registry="ghcr.io",
                 token=os.getenv("GITHUB_TOKEN"),
                 owner=os.getenv("GITHUB_REPOSITORY_OWNER", "Accommodus"),
                 repo=os.getenv("GITHUB_REPOSITORY",
                                "Accommodus/Typst-Editor-devcontainer"),
                 api_url=os.getenv("GITHUB_API_URL", "https://api.github.com"),
                 platforms=["linux/amd64", "linux/arm64"]
                ):
        self.shortname = shortname
        self.dockerfile = dockerfile_path
        self.base_image = base_image

        self.registry = registry
        self.token = token
        self.owner = owner
        self.repo = repo.split("/")[1]
        self.api_url = api_url
        self.platforms = platforms

    def get_name(self):
        return f"{self.registry}/{self.owner}/{self.repo}/{self.short_name}".lower()

    def get_version(self):
        url = f"{self.api_url}/users/{self.owner}/packages/container/{self.repo}%2F{self.short_name}/versions"
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.token}",
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
    

    def build_and_push(self) -> None:
        """
        Build and push a multi-platform Docker image using Buildx with cache support,
        via the python-on-whales DockerClient.
        """

        image_name = self.get_name()
        vers = self.get_version()

        print(f"Pushing {image_name}:v{vers}")

        cache = f"{image_name}:latest"

        # Prepare tags
        tags = [f"{image_name}:v{vers}", f"{image_name}:latest"]

        # Prepare args
        args = {}
        if self.base_image != None:
            args = {"BASE_IMAGE": self.base_image}

        # Run the buildx build
        docker.build(
            context_path="src",
            pull=True,
            file=self.dockerfile,
            platforms=self.platforms,
            tags=tags,
            cache_from=cache,
            cache_to=cache,
            push=False,
            build_args=args
        )


