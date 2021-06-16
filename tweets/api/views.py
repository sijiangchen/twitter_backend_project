from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from tweets.api.serializers import TweetSerializer, TweetSerializerForCreate
from tweets.models import Tweet
from newsfeeds.services import NewsFeedService

class TweetViewSet(viewsets.GenericViewSet):
    #django 默认post的表单
    serializer_class = TweetSerializerForCreate

    #定义各个方法的访问权限
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def list(self,request):
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)
        user_id = request.query_params['user_id']#django 会自动把string转换成int
        tweets = Tweet.objects.filter(user_id=user_id).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True) #返回list of dict
        return Response({'tweets': serializer.data})

    def create(self,request):
        serializer = TweetSerializerForCreate(
            data = request.data,
            context = {'request': request},
        )
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            },status=400)
        #save will trigger create method in TweetSerializerForCreate
        tweet = serializer.save()
        NewsFeedService.fanout_to_followers(tweet)
        return Response(TweetSerializer(tweet).data,status=201)