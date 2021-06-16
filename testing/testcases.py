from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from rest_framework.test import APIClient

class TestCase(DjangoTestCase):

    @property
    def anonymous_client(self):
        #instance level cache
        if hasattr(self,'_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client

    def create_user(self,username,email=None,password=None):
        #不能直接用create 因为password要被加密，username和email需要进行一些normalize处理
        if password is None:
            password = 'generic password'
        if email is None:
            email = f'{username}@twitter.com'
        return User.objects.create_user(username, email, password)

    def create_tweet(self,user,content=None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user,content=content)
