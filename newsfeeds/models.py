from django.db import models
from django.contrib.auth.models import User
from tweets.models import Tweet

class NewsFeed(models.Model):
    #这个user不是存储谁发了这条tweet，而是谁可以看到这条tweet
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user','created_at'),)
        unique_together = (('user','tweet'),)
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'
