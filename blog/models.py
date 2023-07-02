from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("accounts.CustomUser",on_delete=models.CASCADE)
    summaries = models.TextField(max_length=250,null=True,blank=True)
    body = models.TextField()
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("PostDetails", args={str(self.pk)},)
    

