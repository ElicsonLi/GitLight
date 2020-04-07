from django.shortcuts import render, Http404

from gitlight.gitop import repo
from gitlight.utils import *
from gitlight import REPO_PATH


# def test(request):
#     context = {}
#     r = repo.FancyRepo('.')
#     context['tmp'] = r.get_default_branch()
#     return render(request, 'gitlight/index.html', context)

def repo_list(request):
    """Show a list of all repos and can be sorted by last update."""
    valid_repos, invalid_repos = load_repos_name(REPO_PATH)

    context = {}
    context['invalid_repo'] = invalid_repos.keys()
    context['valid_repo'] = valid_repos.keys()

    return render(request, 'gitlight/repo_list.html', context)


def repo_contents(request, repo_name,repo_path=None):
    repo, rev, path, commit = get_repo_rev(repo_name, rev=None, path=REPO_PATH)
    try:
        blob_or_tree = repo.get_blob_or_tree(commit=commit, path=path)
    except KeyError:
        raise NotFound("File not found")

    history = repo.history(commit=commit, path=repo_path)
    if repo_path == None:
        root_tree = repo.listdir(commit=commit, path=path)
    else:
        root_tree = repo.listdir(commit=commit, path=repo_path)


    # send context
    context = {
        'repo': repo,
        'rev': rev,
        'branches': repo.get_branch_names(exclude=rev),
        'tags': repo.get_tag_names(),
        'path': path,
        'blob_or_tree': blob_or_tree,
        'history': history,
        'root_tree': root_tree
    }
    print(history[0].message)
    return render(request, 'gitlight/repo_page.html', context)
