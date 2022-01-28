from __future__ import unicode_literals
import datetime
from django.db import models
from account.models import *


class PostUserUpdate(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
	is_view = models.IntegerField(default=0) 
	post = models.TextField(blank=True,null=True)

	def __str__(self):
		return self.user.name

class PostUserReact(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user_visit")
	
	post = models.ForeignKey(PostUserUpdate, on_delete=models.CASCADE, related_name="post_react")

	def __str__(self):
		return self.user


from django.db import models
from account.models import *


class PostUserUpdate(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
	is_view = models.IntegerField(default=0) 
	post = models.TextField(blank=True,null=True)

	def __str__(self):
		return self.user.name

class PostUserReact(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user_visit")
	
	post = models.ForeignKey(PostUserUpdate, on_delete=models.CASCADE, related_name="post_react")
	
	def __str__(self):
		return self.user

class UserMatchProfile(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_matches")
	like_profile_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_match_user")
	is_like = models.BooleanField(default=False)
	craeted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.name

class UserToUserLike(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to_user")
	like_profile_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
	is_like = models.BooleanField(default=False) 
	craeted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.name

class UserToUserUnLike(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_user_to_unlike")
	like_profile_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_user_profie")
	craeted = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.email
