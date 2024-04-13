import os
import unittest
import shutil

from embedder import RepoEmbedder


class TestCloneRepo(unittest.TestCase):
    def test_clone_repo(self):
        github_url = "https://github.com/Marvin-Deng/Online-Store"
        embedder = RepoEmbedder(github_url)
        repo_path = "./repo/Online-Store"
        self.assertTrue(os.path.exists(repo_path))
        shutil.rmtree("./repo")


if __name__ == "__main__":
    unittest.main()
