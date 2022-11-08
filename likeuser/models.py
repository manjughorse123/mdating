# from django.db import models
# from account.models import *
# # Create your models here.


# class UserLike(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_like")
#     flg = models.BooleanField(default=False)

#     def __str__(self) :
#         return self.user.email


# class UserLikeNew(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like_new")
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_like_new")
#     is_like = models.BooleanField(default=False)

#     def __str__(self) :
#         return self.user

# class UserLikeShare(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like_ne")
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_user_like_ne")
#     # is_like = models.BooleanField(default=False)

#     def __str__(self) :
#         return self.user


# class Matchesprofile(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userpr_like_ne")
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to_ma_user_like_ne")
