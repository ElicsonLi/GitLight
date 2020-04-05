"""This file contains some helper functions"""
import os

from gitlight.gitop.repo import FancyRepo, InvalidRepo
from dulwich.errors import *
from gitlight import REPO_PATH


def load_repos_name(path):
    """Get a dict of repo names and repo objects"""
    valid_repos, invalid_repos = load_repos(path)

    valid_repos = {repo.name: repo for repo in valid_repos}
    invalid_repos = {repo.name: repo for repo in invalid_repos}

    return valid_repos, invalid_repos


def load_repos(repo_path):
    """Load repo object from repo paths"""
    repo_paths = path_to_paths(repo_path)
    valid_repos = []
    invalid_repos = []
    for path in repo_paths:
        try:
            valid_repos.append(FancyRepo(path))
        except NotGitRepository:
            invalid_repos.append(InvalidRepo(path))
    return valid_repos, invalid_repos


def path_to_paths(path):
    """Get top level directories"""
    paths = []
    for folder in os.listdir(path):
        # Check if dir is a directory
        if os.path.isdir(os.path.join(path, folder)):
            paths.append(os.path.join(path, folder))
    return paths


if __name__ == '__main__':
    print(path_to_paths(REPO_PATH))
    valid_repos, invalid_repos = load_repos_name(path_to_paths(REPO_PATH))
    print(valid_repos, invalid_repos)
