import logging
import subprocess
import tarfile
from pathlib import Path

# project names and tags
GITHUB_REPO = {
    "wikimedia/mediawiki": "1.40.1",
    "wikimedia/mediawiki-extensions-cldr": "2023.10",
    "unicode-org/cldr": "release-44",
}


def download_files() -> None:
    download_path = Path("build")
    for repo_name, repo_tag in GITHUB_REPO.items():
        repo_path = download_path / f"{repo_name.rsplit('/', 1)[-1]}-{repo_tag}"
        if not repo_path.is_dir():
            url = f"https://github.com/{repo_name}/archive/refs/tags/{repo_tag}.tar.gz"
            tar_path = download_path / url.rsplit("/", 1)[-1]
            if not tar_path.exists():
                logging.info(f"Downloading {repo_name} {repo_tag}")
                subprocess.run(
                    ["wget", "-nv", "-P", "build", url],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            with tarfile.open(tar_path) as tar:
                logging.info(f"Extracing {repo_name}")
                tar.extractall(download_path)
            tar_path.unlink()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    download_files()
