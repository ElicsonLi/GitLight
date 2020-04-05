from django.shortcuts import render, Http404
from gitlight.gitop import repo


# Create your views here.

def test(request):
    context = {}
    r = repo.FancyRepo('./repos/GitLight')
    context['tmp'] = r.get_default_branch()
    return render(request, 'gitlight/index.html', context)
