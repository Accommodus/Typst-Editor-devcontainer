import os
import subprocess
import requests
from dotenv import load_dotenv
from python_on_whales import docker


class ManageImage():
    def __init__(self,
                 shortname="install-fonts",
                 dockerfile_path="src/install-fonts.Dockerfile",
                 registry="ghcr.io",
                 platforms=["linux/amd64", "linux/arm64"],
                 workspace_folder="src",
                 config="src/devcontainer.json",
                 token=None,
                 owner=None,
                 repo=None,
                 api_url=None
                 ):

        load_dotenv()

        if token == None:
            token = os.getenv("GITHUB_TOKEN")

        if owner == None:
            owner = os.getenv("GITHUB_REPOSITORY_OWNER", "Accommodus")

        if repo == None:
            repo = os.getenv("GITHUB_REPOSITORY",
                             "Accommodus/Typst-Editor-devcontainer")

        if api_url == None:
            api_url = os.getenv("GITHUB_API_URL", "https://api.github.com")

        self.shortname = shortname
        self.dockerfile = dockerfile_path

        self.registry = registry
        self.platforms = platforms

        self.workspace_folder = workspace_folder
        self.config = config

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

    def build_base(self) -> None:
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
        tags = [f"{image_name}:v{vers}", f"{image_name}:latest"]

        # Run the buildx build
        docker.build(
            context_path="src",
            pull=True,
            file=self.dockerfile,
            platforms=self.platforms,
            tags=tags,
            cache_from=cache,
            cache_to=cache,
            push=True,
        )

    def prebuild(self, extend=None):
        print("Logging in...")
        docker.login(server=self.registry, username=self.owner, password=self.token)

        prebuilt_name = f"{self.registry}/{self.owner}/{self.repo}".lower()
        if extend != None:
            prebuilt_name += f"/{extend}".lower()

        latest = f"{prebuilt_name}:latest"
        cache = f"{prebuilt_name}:cache"
        platforms = ",".join(self.platforms)

        cmd = [
            "devcontainer", "build",
            "--workspace-folder", self.workspace_folder,
            "--config", self.config,
            "--push", "true",
            "--image-name", latest,
            "--cache-from", cache,
            "--cache-to", cache,
            "--platform", platforms
        ]

        out = subprocess.run(cmd, check=True, text=True)
        print(out)

def build_fonts_install():
    install = ManageImage()
    install.build_base()

def prebuild():
    install = ManageImage()
    install.prebuild()

def build_meta():
    meta = ManageImage(workspace_folder=".devcontainer", config=".devcontainer/devcontainer.json")
    meta.prebuild(extend="meta_container")

if __name__ == "__main__":
    #build_fonts_install()
    #prebuild()
    build_meta()
