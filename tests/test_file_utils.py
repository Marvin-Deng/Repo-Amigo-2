import unittest
import shutil


from file_utils import (
    clone_repo,
    get_text_chunks,
)


class TestCloneRepo(unittest.TestCase):
    def test_clone_repo(self):
        github_url = "https://github.com/Marvin-Deng/Online-Store"
        repo_path = "./repo/Online-Store"
        self.assertTrue(clone_repo(github_url, repo_path))
        shutil.rmtree("./repo")


if __name__ == "__main__":
    unittest.main()
