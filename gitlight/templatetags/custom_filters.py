from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
import re

register = template.Library()


@register.filter(name='shorten_commit_content')
# @stringfilter
def shorten_commit_content(msg):
    # remove b' and \n'
    # print(msg.split('\\n')[0])
    return msg.decode("utf-8")


@register.filter(name='unix_time_to_datatime')
def unix_time_to_datatime(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object


@register.filter(name='extract_author_name')
@stringfilter
def extract_author_name(author_email):
    """Display name if there is any, or email address if there is no name specified."""
    author_email = author_email[2:-1]
    match = re.match('^(.*?)<.*?>$', author_email)
    if match:
        return match.group(1).strip()
    return author_email
