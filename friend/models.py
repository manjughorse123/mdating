from django.db import models
from django.conf import settings
from django.utils import timezone
from account.models import *



class FriendList(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
	# friends = models.ManyToManyField(User, blank=True, related_name="friends") 
	friends = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="friends")

	def __str__(self):
		return self.user.name

	def add_friend(self, account):
		"""
		Add a new friend.
		"""
		if not account in self.friends.all():
			self.friends.add(account)
			self.save()

	def remove_friend(self, account):
		"""
		Remove a friend.
		"""
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		"""
		Initiate the action of unfriending someone.
		"""
		remover_friends_list = self # person terminating the friendship

		# Remove friend from remover friend list
		remover_friends_list.remove_friend(removee)

		# Remove friend from removee friend list
		friends_list = FriendList.objects.get(user=removee)
		friends_list.remove_friend(remover_friends_list.user)


	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		return False


class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 				= models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
	receiver 			= models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver",)

	is_active			= models.BooleanField(blank=False, null=False, default=True)

	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.name



class FollowRequest(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_user")
	# friends = models.ManyToManyField(User, blank=True, related_name="friends") 
	follow = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="Follow_user")
	is_active			= models.BooleanField(blank=False, null=False, default=True)

	timestamp 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.name


class FollowAccept(models.Model):

	user 	= models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent_user_accept")
	# friends = models.ManyToManyField(User, blank=True, related_name="friends") 
	follow = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="Follow_user_accept")



	def __str__(self):
		return self.follow.name


class FAQ(models.Model):

	question = models.CharField(max_length=255)
	answer = models.TextField(blank=True ,null=True)
	create_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.question



