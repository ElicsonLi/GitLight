from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('create_repo', views.create_repo_action, name='create_repo'),
    path('<str:repo_name>', views.repo_contents, name='repo_contents'),
    path('issue/<str:repo_name>', views.issue_page, name='issue_page'),
    path('create_issue_page/<str:repo_name>', views.create_issue_page, name='create_issue_page'),
    path('create_issue/<str:repo_name>', views.create_issue, name='create_issue'),
    path('tree/<str:repo_name>/<path:repo_path>', views.repo_contents, name='repo_contents'),
    path('blob/<str:repo_name>/<path:repo_path>', views.file_view, name='file_view')
]
