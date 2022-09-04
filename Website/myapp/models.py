from django.db import models
from django.db import models
from datetime import datetime

    
class Message(models.Model):
    text = models.CharField(max_length=1000000)
    date = models.DateTimeField(default = datetime.now, blank=True)
    # user_id = models.IntegerField(max_length=1000000)
    username = models.CharField(max_length=1000000)


# class signup(models.Model):
#     name = models.CharField(max_length=25)
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=15)
    
# class Data(models.Model):
#     name = models.CharField(max_length=25)
        