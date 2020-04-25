from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField


# Create your models here.
# class Profile(models.Model):
#     """Profile class specifies a user's profile"""
#     user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
#     bio_input_text = models.CharField(max_length=10000)
#     profile_picture = models.FileField(blank=True)
#     content_type = models.CharField(max_length=50)
#     ip_addr = models.GenericIPAddressField(default=None)
#     follows = models.ManyToManyField('Profile', related_name='followed_by')

class RepoModel(models.Model):
    """A mapping from git repo to django model"""
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)


class Issue(models.Model):
    belong_to = models.ForeignKey(
        'RepoModel', default=None, on_delete=models.PROTECT)
    # Title of Issue
    title = models.CharField(
        max_length=100)
    # Content of issue
    content = MDTextField()

    # Indicate whether a issue has been solved
    SOLVED = 'T'
    UNSOLVED = 'F'
    SOLVED_CHOICES = [
        (SOLVED, 'solved'),
        (UNSOLVED, 'unsolved'),
    ]
    solved_state = models.CharField(
        max_length=1,
        choices=SOLVED_CHOICES,
        default=UNSOLVED,
    )


class Reply(models.Model):
    belong_to = models.ForeignKey(
        'Issue', default=None, on_delete=models.PROTECT)
    # Content of issue
    content = MDTextField()

class Profile(models.Model):
    bio_input_text = models.CharField(max_length=200)
    update_time = models.DateTimeField()
    profile_picture = models.FileField(blank=True)
    profile_user_id = models.IntegerField()
    content_type = models.CharField(max_length=50)
    update_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="profile_updates")

    def __str__(self):
        return str(self.update_by)+" "+self.bio_input_text

