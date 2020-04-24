import sys
from django.shortcuts import render, redirect, Http404, HttpResponse

from django.urls import reverse
from django.core.exceptions import *
from gitlight.models import RepoModel, Issue, Reply
from gitlight.gitop import repo, utils
from gitlight.utils import *
from gitlight import REPO_PATH, IP_ADDR
import markdown

from gitlight.gitop import markup
from gitlight.gitop.highlighting import highlight_or_render

# login/ register actions
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from gitlight.forms import LoginForm, RegistrationForm, IssueForm


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

    if commit is not None:
        try:
            blob_or_tree = repo.get_blob_or_tree(commit=commit, path=path)
        except KeyError:
            raise NotFound("File not found")

        # Support for directory display
        history = repo.history(commit=commit, path=repo_path)
        if repo_path is None:
            root_tree = repo.listdir(commit=commit, path=path)
        else:
            root_tree = repo.listdir(commit=commit, path=repo_path)

    if rev is None:
        context = {
            'path': 'This is an empty dir',
            'repo': repo,
            'rev': rev,
        }
        return render(request, 'gitlight/repo_page.html', context)

    # send context
    context = {
        'repo': repo,
        'rev': rev,
        'branches': repo.get_branch_names(exclude=rev),
        'tags': repo.get_tag_names(),
        'path': path,
        'commit': commit,
        'blob_or_tree': blob_or_tree,
        'history': history,
        'root_tree': root_tree,
        'ip_addr': IP_ADDR,
    }
    print(commit.id)
    return render(request, 'gitlight/repo_page.html', context)


def file_view(request, repo_name, repo_path=None):
    repo, rev, path, commit = get_repo_rev(repo_name, rev=None, path=REPO_PATH)
    try:
        blob_or_tree = repo.get_blob_or_tree(commit=commit, path=repo_path)
    except KeyError:
        raise NotFound("File not found")
    filename = os.path.basename(repo_path)
    lastindex = repo_path.rfind('/')
    if (lastindex < 0):
        upperdir = path
    else:
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
        'render_code': highlight_or_render(blob_or_tree.data, filename),
        'root_tree': root_tree
    }
    return render(request, 'gitlight/file_view.html', context)


def create_repo_action(request):
    if request.method == 'GET':
        raise Http404

    create_repo(request.POST['repo_name'])

    # Create repo model
    new_repo = RepoModel(name=request.POST['repo_name'], user=request.user)
    new_repo.save()

    return redirect(reverse('repo_list'))


def issue_list_page(request, repo_name):
    try:
        belong_to = RepoModel.objects.get(name=repo_name)
    except ObjectDoesNotExist:
        return HttpResponse("Repo not created on this website!")
    issues = Issue.objects.filter(belong_to=belong_to).all()
    context = {'repo_name': repo_name,
               'issues': issues}
    return render(request, 'gitlight/issue_list.html', context)


def create_issue(request, repo_name):
    if request.method == 'GET':
        raise Http404
    # Create issue under a repo
    try:
        belong_to = RepoModel.objects.get(name=repo_name)
    except ObjectDoesNotExist:
        raise Http404
    new_issue = Issue(belong_to=belong_to, title=request.POST['issue_title'], content=request.POST['content'])
    new_issue.save()

    return redirect(reverse('issue_list_page', args=[repo_name]))


def create_issue_page(request, repo_name):
    editor = IssueForm()
    context = {'repo_name': repo_name,
               'editor': editor}
    return render(request, 'gitlight/create_issue_page.html', context)


def view_diff(request, repo_name, commit_id):
    repo, rev, path, commit = get_repo_rev(repo_name, rev=None, path=REPO_PATH)
    this_commit = repo.get_commit(commit_id)
    summary, file_changes = repo.commit_diff(this_commit)
    context = {
        'repo': repo,
        'file_changes': file_changes,
        'summary': summary
    }
    return render(request, 'gitlight/diff_view.html', context)


def issue_detail_page(request, issue_id):
    # issue = Issue.objects.get(id=issue_id)
    # context = {'issue': issue}
    try:
        issue = Issue.objects.get(pk=int(issue_id))
    except:
        return HttpResponse('No such issue')
    issue.content = markdown.markdown(issue.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    # Reply editor
    editor = IssueForm()
    # Get all replies
    replies = Reply.objects.filter(belong_to=issue).all()
    # Format all replies
    for reply in replies:
        reply.content = markdown.markdown(reply.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    context = {'issue': issue,
               'editor': editor,
               'replies': replies}
    return render(request, 'gitlight/issue_detail.html', context)


def create_reply(request, issue_id):
    if request.method == 'GET':
        raise Http404
    # Create issue under a repo
    try:
        belong_to = Issue.objects.get(id=issue_id)
    except ObjectDoesNotExist:
        raise Http404
    new_reply = Reply(belong_to=belong_to, content=request.POST['content'])
    new_reply.save()

    return redirect(reverse('issue_detail_page', args=[issue_id]))
