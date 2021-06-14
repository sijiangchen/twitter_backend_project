from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import (
    UserSerializer,
    LoginSerializer,
    SignupSerializer,
)
from django.contrib.auth import(
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate
)
class UserViewSet(viewsets.ModelViewSet):
    #若不支持增删查改，可以改成viewsets.ReadOnlyModelViewSet
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]#必须登陆才能操作
    # permission_classes = [permissions.AllowAny]

class AccountViewSet(viewsets.ViewSet):
    serializer_class= SignupSerializer
    @action(methods=['GET'],detail=False)#detail=false 说明是定义在整个accounts上的动作，=true说明是定义在某个object上的动作
    def login_status(self,request):
        data={'has_logged_in': request.user.is_authenticated,
              'ip': request.META['REMOTE_ADDR']}
        if request.user.is_authenticated:
            data['user']=UserSerializer(request.user).data
        return Response(data)

    @action(methods=['POST'],detail=False)
    def logout(self,request):
        django_logout(request)
        return Response({'success':True})

    @action(methods=['POST'],detail=False)
    def login(self,request):
        #get username and password from requests
        serializer = LoginSerializer(data=request.data)# 如果是GET:request.query_params
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please Check input",
                "errors": serializer.errors,
            },status=400)#默认status是200
        #validation ok, login
        username = serializer.validated_data['username'].lower()
        password = serializer.validated_data['password']

        #user doesn't exist
        if not User.objects.filter(username=username).exists():
            # queryset=User.objects.filter(username=username)
            #print(queryset.query) 打印语句
            return Response({
                "success": False,
                "message": "User does not exist.",
            }, status=400)

        user = django_authenticate(username=username,password=password)
        if not user or user.is_anonymous:
            return Response({
                "success": False,
                "message": "Username and password doesn not match.",
            },status=400)
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        }, status=200)

    @action(methods=['POST'],detail=False)
    def signup(self,request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors,
            }, status=400)

        user = serializer.save()#create a new user
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(user).data,
        }, status=201)
