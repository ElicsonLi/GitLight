"""This file contains some helper functions"""
from os import mkdir,chdir
import os
import sys

from gitlight.gitop.repo import FancyRepo, InvalidRepo
from dulwich.errors import *
from dulwich.repo import Repo
from gitlight import REPO_PATH

from werkzeug.wrappers import Response
from werkzeug.exceptions import NotFound


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


def get_repo_rev(repo, rev=None, path=None):
    """fetch repo from repo list"""
    if path and rev:
        rev += "/" + path.rstrip("/")

    valid_repos, invalid_repos = load_repos_name(path)

    # Try to find repo in valid repo list
    try:
        repo = valid_repos[repo]
    except KeyError:
        raise NotFound("No such repository %r" % repo)

    # if branch not specify
    if rev is None:
        rev = repo.get_default_branch()
        commit = None

    # Try to get default commit
    if rev is not None:
        i = len(rev)
        while i > 0:
            try:
                commit = repo.get_commit(rev[:i])
                path = rev[i:].strip("/")
                rev = rev[:i]
            except (KeyError, IOError):
                i = rev.rfind("/", 0, i)
            else:
                break
        else:
            raise NotFound("No such commit %r" % rev)
    return repo, rev, path, commit


def create_repo(repo_name):
    """Create a new repo and return to the new repo project"""
    # chdir(REPO_PATH)
    path = REPO_PATH+'/'+repo_name
    try:
        mkdir(path)
        new_repo = Repo.init(path)
        return new_repo
    except OSError:
        raise NotFound("Path not legal")

if __name__ == '__main__':
    REPO_PATH_DBG = '../repos'
    print(path_to_paths(REPO_PATH_DBG))
    valid_repos, invalid_repos = load_repos_name(REPO_PATH_DBG)
    print(valid_repos, invalid_repos)
    repo, rev, path, commit = get_repo_rev('websockets-example', rev=None, path=None)
    print(commit)
