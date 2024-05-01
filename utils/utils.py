import re


def is_valid_github_url(url):
    if url == "":  # Empty url doesn't change the state
        return True
    regex = r"https?:\/\/(www\.)?github\.com\/[\w-]+\/[\w-]+"
    if re.match(regex, url):
        return True
    return False
