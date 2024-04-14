import unittest
from unittest.mock import MagicMock, patch
from repo_chain.chain import RepoChain


class TestChain(unittest.TestCase):
    @patch("os.path.exists")
    @patch("chain.FAISS")
    def test_load_faiss_index_with_existing_path(
        self, FAISS_mock, exists_mock
    ):
        FAISS_mock.load_local.return_value = MagicMock()
        exists_mock.return_value = True

        index_path = "test_index_path"
        chain = RepoChain(index_path)

        result = chain.load_faiss_index()

        self.assertEqual(chain.index_path, index_path)
        FAISS_mock.load_local.assert_called_once()
        self.assertIsNotNone(result)

    @patch("os.path.exists")
    @patch("chain.FAISS")
    def test_load_faiss_index_with_non_existing_path(
        self, FAISS_mock, exists_mock
    ):
        FAISS_mock.load_local.return_value = MagicMock()
        exists_mock.return_value = False

        index_path = "non_existing_index_path"
        chain = RepoChain(index_path)

        result = chain.load_faiss_index()

        self.assertEqual(chain.index_path, index_path)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
