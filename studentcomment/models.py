from django.db import models
from django.contrib.auth.models import AbstractUser,User
from SchoolComment import settings

class MainComment(models.Model):
    main_comment_text=models.TextField(max_length=400)
    created_time_stamp=models.DateTimeField(auto_now_add=True)
    latest_change_time_stamp=models.DateTimeField(auto_now_add=True,null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return  self.comment_text

    class Meta:
        permissions=(
            ("change_comment","Can change the comment"),
            ("look_up_all","Can look up all comments"),
        )

class OtherComments(models.Model):
    user_to=models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_to",null=True)
    other_comment_text = models.TextField(max_length=400)
    created_time_stamp = models.DateTimeField(auto_now_add=True)
    latest_change_time_stamp = models.DateTimeField(auto_now_add=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="author",null=True)

    def __str__(self):
        return self.other_comment_text

    class Meta:
        permissions=(
            ("change_comment","Can change the comment"),
            ("look_up_all","Can look up all comments"),
        )
