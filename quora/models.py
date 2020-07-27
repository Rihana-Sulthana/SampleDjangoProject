from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


# Create your models here.
class AbstractModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, AbstractModel):
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=250, null=False, blank=False)
    object = UserManager()

    USERNAME_FIELD = 'email'

class Questions(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()


class Answers(AbstractModel):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.TextField()
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)

class UpVotes(AbstractModel):
    answer = models.ForeignKey(Answers, on_delete=models.CASCADE)
    upvoted_by = models.ForeignKey(User, on_delete=models.CASCADE)

