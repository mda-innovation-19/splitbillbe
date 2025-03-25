from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    account_number = models.CharField(max_length=13, blank=True, null=True)
    balance = models.IntegerField(default=0)

class Friendship(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')