from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
#login/后面的/必须要打
LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout/'
SIGNUP_URL = '/api/accounts/signup/'
LOGIN_STATUS_URL = '/api/accounts/login_status/'
# Create your tests here.

class AccountApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@jiuzhang.com',
            password='correct password',
        )

    def createUser(self,username,email,password):
        #不能直接用create 因为password要被加密，username和email需要进行一些normalize处理
        return User.objects.create_user(username, email, password)

    def test_login(self):
        #测试必须用post而不是get
        response= self.client.get(LOGIN_URL,{
            'username':self.user.username,
            'password':'correct password',
        })
        self.assertEqual(response.status_code,405)

        #用了post但是密码错了
        response=self.client.post(LOGIN_URL, {
            'username':self.user.username,
            'password':'wrong password',
        })
        self.assertEqual(response.status_code,400)

        #验证还没有登陆
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'],False)

        #用正确的密码
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'],None)
        self.assertEqual(response.data['user']['email'],'admin@jiuzhang.com')
        #验证已经登陆了
        response=self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

        #测试用户名正确
        response = self.client.post(LOGIN_URL,{
            'username':'notexists',
            'password':'correct password',
        })
        self.assertEqual(response.status_code,400)
        self.assertEqual(response.data['message'],'User does not exist.')
        # self.assertEqual(str(response.data['errors']['username'][0]),'User does not exist.')
    def test_logout(self):
        #先登录
        self.client.post(LOGIN_URL,{
            'username':self.user.username,
            'password':'correct password',
        })
        #验证用户已经登陆
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'],True)

        #测试必须用post
        response = self.client.get(LOGOUT_URL)
        self.assertEqual(response.status_code, 405)

        #改用post 成功logout
        response = self.client.post(LOGOUT_URL)
        self.assertEqual(response.status_code,200)
        #验证用户已经登出
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'],False)

    def test_signup(self):
        data = {
            'username':'someone',
            'email':'someone@jiuzhang.com',
            'password':'any password',
        }
        #测试get请求失败
        response = self.client.get(SIGNUP_URL,data)
        self.assertEqual(response.status_code,405)

        #测试错误的邮箱
        response = self.client.post(SIGNUP_URL,{
            'username':'someone',
            'email':'not a correct email',
            'password':'any password',
        })
        print(response.data)
        self.assertEqual(response.status_code,400)

        #测试密码太短
        response = self.client.post(SIGNUP_URL,{
            'username':'someone',
            'email':'someone@jiuzhang.com',
            'password':'123',
        })
        print(response.data)
        self.assertEqual(response.status_code,400)

        #测试用户名太长
        response = self.client.post(SIGNUP_URL,{
            'username':'username is tooooooooooooooooooo looooooooooooooooog',
            'email':'someone@jiuzhang.com',
            'password':'any password',
        })
        print(response.data)
        self.assertEqual(response.status_code,400)

        #成功注册
        response = self.client.post(SIGNUP_URL,data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.data['user']['username'],'someone')
        #验证已经登陆
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'],True)




