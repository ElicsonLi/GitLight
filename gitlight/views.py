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

    return render(request, 'gitlight/index.html', context)