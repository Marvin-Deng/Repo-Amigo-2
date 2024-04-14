import os
import unittest
import shutil
from urllib.parse import urlparse

from repo_chain.embedder import RepoEmbedder


class TestRepoEmbedder(unittest.TestCase):
    def setUp(self):
        github_url = "https://github.com/Marvin-Deng/Online-Store"
        repo_name = urlparse(github_url).path.split("/")[1]
        self.embedder = RepoEmbedder(github_url, repo_name)

    def tearDown(self):
        if hasattr(self, "embedder"):
            index_path = self.embedder.index_path

            if os.path.exists(index_path):
                shutil.rmtree("./store")
                print(f"Directory '{index_path}' successfully removed.")

    def test_clone_repo(self):
        self.embedder.clone_repo()
        repo_path = self.embedder.repo_path
        self.assertTrue(os.path.exists(repo_path))

    def test_generate_vector_store(self):
        self.embedder.generate_vector_store()
        index_path = self.embedder.index_path
        self.assertTrue(os.path.exists(index_path))


if __name__ == "__main__":
    unittest.main()
