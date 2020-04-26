# GitLight

## Attention

Git server requires ssh key to access git repository. Users without their key in git server's .ssh/authorized_keys will only be able to create repo and come up with issues. Authorized user (have their key in .ssh/authorized_keys) will be able to clone/push repos.

Steps to create a ssh key.

1. Create ssh key by typein `ssh-keygen` in your shell.

2. Your ssh key should now in your .ssh/id_rsa by default.

3. Copy and paste to git server's .ssh/authorized_keys file

## Demo Link

http://3.20.246.26/

Or

3.20.246.26:8000

## Introdution

Our project is building a website with git service that can be used by students, individual developers and small business. 

## Environment

`pip install humanize werkzeug dulwich httpauth pygments django-mdeditor `

## Functionalities

* Register and Login
	* Need a valid account to login
	* Email Authentication

* Git operations
	* Create a repo
	* Clone the repo
	* Git pull and push

* Basic view functions
	* View all repos
	* View commit of different level
	* View the code and other type of files
	* View changes of all past version

* Issue and Discussion
	* Come up with an issue regarding bugs or suggestions
	* For the issue, others can follow with discussions

* User profile
	* Include a profile picture and bio of the user
	* All of the repos the user have
