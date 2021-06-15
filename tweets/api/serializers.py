from rest_framework import serializers
from tweets.models import Tweet
from accounts.api.serializers import UserSerializerForTweet


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id','user','created_at','content')


class TweetSerializerForCreate(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)#不能放userid进去

    def create(self,validated_data):
        user = self.context['request'].user #context的使用很重要
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user,content=content)
        return tweet
