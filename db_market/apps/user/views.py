from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin
from . import serializer
from db_market.utils.response import APIResponse
from rest_framework.decorators import action
from . import models


class LoginView(ViewSet):
    @action(methods=('post',), detail=False)
    def login(self, request, *args, **kwargs):
        ser = serializer.UserSerilaizer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['user'].username
            return APIResponse(token=token, username=username)
        else:
            return APIResponse(code=0,msg=ser.errors)

    @action(detail=False)
    def check_telephone(self, request, *args, **kwargs):
        import re
        telephone = request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        try:
            models.User.objects.get(telephone=telephone)
            return APIResponse(code=1)
        except:
            return APIResponse(code=0,msg='手机号不存在')

    @action(methods=['POST'],detail=False)
    def code_login(self,request,):
        ser = serializer.CodeUserSerializer(data=request.data)
        if ser.is_valid():
            token = ser.context['token']
            username = ser.context['username']
            return APIResponse(token=token,username=username)
        else:
            return APIResponse(code=0,msg=ser.errors)

from .throttings import SMSThrotting
class SendSmSView(ViewSet):
    throttle_classes = [SMSThrotting,]
    @action(methods=['GET'],detail=False)
    def send(self, request, *args, **kwargs):
        #发送验证码接口
        import re
        from db_market.libs.tx_sms import get_code, send_message
        from django.core.cache import cache
        from django.conf import settings
        telephone =request.query_params.get('telephone')
        if not re.match('^1[3-9][0-9]{9}', telephone):
            return APIResponse(code=0, msg='手机号不合法')
        code=get_code()
        result = send_message(telephone,code)
        #验证码保存到sms_cache_%s
        cache.set(settings.PHONE_CACHE_KEY%telephone,code,180)
        if result:
            return APIResponse(code=1,msg='验证码发送成功')
        else:
            return APIResponse(code=0, msg='验证码发送失败')


class RegisterView(GenericViewSet,CreateModelMixin):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = response.data.get('username')
        return APIResponse(code=1,msg='注册成功',username=username)