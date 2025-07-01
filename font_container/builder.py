import os
import requests
from dotenv import load_dotenv
from python_on_whales import docker

class ManageImage():
    def __init__(self,
                 shortname: str,
                 dockerfile_path: str,
                 base_image=None,
                 registry="ghcr.io",
                 platforms=["linux/amd64", "linux/arm64"],
                 token=None,
                 owner=None,
                 repo=None,
                 api_url=None
                ):
        
        if token == None:
            token = os.getenv("GITHUB_TOKEN")

        if owner == None:
            owner = os.getenv("GITHUB_REPOSITORY_OWNER", "Accommodus")

        if repo == None:
            repo = os.getenv("GITHUB_REPOSITORY", "Accommodus/Typst-Editor-devcontainer")

        if api_url == None:
            api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")


        self.shortname = shortname
        self.dockerfile = dockerfile_path
        self.base_image = base_image

        self.registry = registry
        self.platforms = platforms
        self.token = token
        self.owner = owner
        self.repo = repo.split("/")[1]
        self.api_url = api_url

    def get_name(self) -> str:
        name = f"{self.registry}/{self.owner}/{self.repo}/{self.shortname}".lower()
        print(f"Name: {name}")
        return name

    def get_version(self) -> int:
        url = f"{self.api_url}/users/{self.owner}/packages/container/{self.repo}%2F{self.shortname}/versions"
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
        print("Logging in...")
        docker.login(server=self.registry, username=self.owner, password=self.token)

        image_name = self.get_name()
        vers = str(self.get_version() + 1)

        print(f"Pushing {image_name}:v{vers}")

        cache = f"{image_name}:cache"

        # Prepare tags
        tags = [f"v{vers}", "latest"]

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

def build_fonts_install():
    load_dotenv(verbose=True)

    install = ManageImage("install-fonts", "font_container/Dockerfile")
    install.build_and_push()

if __name__ == "__main__":
    build_fonts_install()