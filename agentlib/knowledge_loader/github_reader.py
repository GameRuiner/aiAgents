import io
import zipfile
import requests
import frontmatter
from typing import List, Dict

class GitHubReader:
    def __init__(self, repo_owner: str, repo_name: str, branch: str = "main"):
        self.owner = repo_owner
        self.repo = repo_name
        self.branch = branch

    def _make_url(self) -> str:
        prefix = "https://codeload.github.com"
        return f"{prefix}/{self.owner}/{self.repo}/zip/refs/heads/{self.branch}"

    def read_repository(self) -> List[Dict]:
        """Download and parse all markdown files from a GitHub repository."""
        url = self._make_url()
        resp = requests.get(url)

        if resp.status_code != 200:
            raise RuntimeError(f"Failed to download repository: {resp.status_code}")

        repository_data = []
        zf = zipfile.ZipFile(io.BytesIO(resp.content))

        for file_info in zf.infolist():
            filename = file_info.filename.lower()
            if not (filename.endswith(".md") or filename.endswith(".mdx")):
                continue

            try:
                with zf.open(file_info) as f_in:
                    content = f_in.read().decode("utf-8", errors="ignore")
                    post = frontmatter.loads(content)
                    data = post.to_dict()
                    data["filename"] = file_info.filename
                    repository_data.append(data)
            except Exception as e:
                print(f"Error processing {file_info.filename}: {e}")

        return repository_data