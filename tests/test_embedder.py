import os
import unittest
import shutil

from embedder import RepoEmbedder


class TestRepoEmbedder(unittest.TestCase):
    def setUp(self):
        github_url = "https://github.com/Marvin-Deng/Online-Store"
        self.embedder = RepoEmbedder(github_url)

    def test_get_repo_name(self):
        self.embedder.get_repo_name()

    def test_clone_repo(self):
        self.embedder.clone_repo()
        repo_path = self.embedder.repo_path
        self.assertTrue(os.path.exists(repo_path))

    def test_generate_vector_store(self):
        self.embedder.generate_vector_store()
        embeddings_path = self.embedder.embeddings_path
        self.assertTrue(os.path.exists(embeddings_path))


if __name__ == "__main__":
    unittest.main()
