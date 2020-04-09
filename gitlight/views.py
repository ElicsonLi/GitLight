import sys
from django.shortcuts import render, redirect

from django.urls import reverse

from gitlight.gitop import repo, utils
from gitlight.utils import *
from gitlight import REPO_PATH


from gitlight.gitop import markup
from gitlight.gitop.highlighting import highlight_or_render

# login/ register actions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from gitlight.forms import LoginForm, RegistrationForm

try:
    import ctags
except ImportError:
    ctags = None
else:
    from gitlight.gitop import ctagscache
    CTAGS_CACHE = ctagscache.CTagsCache()


def login_action(request):
    context = {}
    # Display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'gitlight/login.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'gitlight/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    # # create default when profile does not exist
    # if not Profile.objects.filter(user=new_user).exists():
    #     profile = Profile(user=new_user, id=new_user.id,
    #                       ip_addr=request.META['REMOTE_ADDR'])
    #     profile.save()
    login(request, new_user)
    return redirect(reverse('repo_list'))


def register_action(request):
    context = {}

    # Display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'gitlight/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'gitlight/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    # # create default when profile does not exist
    # if not Profile.objects.filter(user=new_user).exists():
    #     profile = Profile(user=new_user, id=new_user.id,
    #                       ip_addr=request.META['REMOTE_ADDR'])
    #     profile.save()

    login(request, new_user)
    return redirect(reverse('repo_list'))


@login_required
def repo_list(request):
    """Show a list of all repos and can be sorted by last update."""
    valid_repos, invalid_repos = load_repos_name(REPO_PATH)

    context = {}
    context['invalid_repo'] = invalid_repos.keys()
    context['valid_repo'] = valid_repos.keys()

    return render(request, 'gitlight/repo_list.html', context)


@login_required
def repo_contents(request, repo_name, repo_path=None):
    repo, rev, path, commit = get_repo_rev(repo_name, rev=None, path=REPO_PATH)
    try:
        blob_or_tree = repo.get_blob_or_tree(commit=commit, path=path)
    except KeyError:
        raise NotFound("File not found")

    # Support for directory display
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
    return render(request, 'gitlight/repo_page.html', context)


def file_view(request,repo_name,repo_path=None):
    repo, rev, path, commit = get_repo_rev(repo_name, rev=None, path=REPO_PATH)
    try:
        blob_or_tree = repo.get_blob_or_tree(commit=commit, path=repo_path)
    except KeyError:
        raise NotFound("File not found")
    filename = os.path.basename(repo_path)
    lastindex = repo_path.rfind('/')
    upperdir = repo_path[:lastindex]
    root_tree = repo.listdir(commit=commit, path=upperdir)
    context = {
        'repo': repo,
        'rev': rev,
        'branches': repo.get_branch_names(exclude=rev),
        'tags': repo.get_tag_names(),
        'path': path,
        'blob_or_tree': blob_or_tree,
        'filename': filename,
        'render_code' : highlight_or_render(blob_or_tree.data,filename),
        'root_tree': root_tree
    }
    return render(request, 'gitlight/file_view.html', context)
