from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.repo_list, name='repo_list'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('profile', views.accssemyprofile_action, name='profile_page'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('create_repo', views.create_repo_action, name='create_repo'),
    path('<str:repo_name>', views.repo_contents, name='repo_contents'),
    path('issue/<str:repo_name>', views.issue_list_page, name='issue_list_page'),
    path('issue_detail/<int:issue_id>', views.issue_detail_page, name='issue_detail_page'),
    path('create_issue_page/<str:repo_name>', views.create_issue_page, name='create_issue_page'),
    path('create_issue/<str:repo_name>', views.create_issue, name='create_issue'),
    path('create_reply/<int:issue_id>', views.create_reply, name='create_reply'),
    path('tree/<str:repo_name>/<path:repo_path>', views.repo_contents, name='repo_contents'),
    path('blob/<str:repo_name>/<path:repo_path>', views.file_view, name='file_view'),
    path('commit/<str:repo_name>/<str:commit_id>', views.view_diff, name='view_diff'),
]
