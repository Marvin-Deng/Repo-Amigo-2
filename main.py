from file_utils import (
    clone_repo,
    recursively_parse_repo_files
)

def main():
    github_url = "https://github.com/Marvin-Deng/Online-Store"
    repo_path = "./repo/Online-Store"
    clone_repo(github_url, repo_path)
    recursively_parse_repo_files(repo_path)

if __name__ == '__main__':
    main()