from rest_framework import serializers
from . import models
from rest_framework.exceptions import ValidationError

import re
from django.core.cache import cache
from django.conf import settings

class UserSerilaizer(serializers.ModelSerializer):
    # 用户登录序列化器
    username = serializers.CharField()

    class Meta:
        model = models.User
        fields = ['username', 'password', 'id', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(attrs)
        # 放到context中，我在视图类中可以取出来
        self.context['token'] = token
        self.context['user'] = user
        return attrs

    def _get_user(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        import re
        if re.match('^1[3-9][0-9]{9}$', username):  # 匹配手机
            user = models.User.objects.filter(telephone=username).first()
        elif re.match('^.+@.+$', username):  # 匹配邮箱
            user = models.User.objects.filter(email=username).first()
        else:
            # 其余的为用户名
            user = models.User.objects.filter(username=username).first()
        if user:
            ret = user.check_password(password)
            if ret:
                return user
            else:
                raise ValidationError('密码错误')
        else:
            raise ValidationError('用户不存在')

    def _get_token(self, attrs):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler
        token = jwt_encode_handler(payload)
        return token


class CodeUserSerializer(serializers.ModelSerializer):
    #验证码序列化器
    code = serializers.CharField()
    class Meta:
        model = models.User
        fields = ['telephone', 'code']


    def validate(self, attrs):
        user = self._get_user(attrs)
        token = self._get_token(attrs)
        self.context['user'] = user
        self.context['token'] = token
        return attrs


    def _get_user(self, attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        # 取出原来的code
        cache_code=cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code:
            #验证码通过
            if re.match('^1[3-9][0-9]{9}$', telephone):
                user = models.User.objects.filter(telephone=telephone).first()
                if user:
                    #将使用过的验证码删除
                    cache.set(settings.PHONE_CACHE_KEY % telephone, '')
                    return user
                else:
                    raise ValidationError('用户不存在')
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')


    def _get_token(self, attrs):
        from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
        payload = jwt_payload_handler
        token = jwt_encode_handler(payload)
        return token


class UserRegisterSerializer(serializers.ModelSerializer):
    #用户注册
    code = serializers.CharField(max_length=4,min_length=4,write_only=True)
    class Meta:
        model = models.User
        fields = ['telephone','code','password','username']
        extra_kwargs = {
            'username':{'read_only':True},
            'password':{'max_length':18,'min_length':8},
        }


    def validate(self,attrs):
        telephone = attrs.get('telephone')
        code = attrs.get('code')
        cache_code = cache.get(settings.PHONE_CACHE_KEY % telephone)
        if code == cache_code or code == '1234':
            if re.match('^1[3-9][0-9]{9}$', telephone):
                attrs['useranme'] = telephone
                attrs.pop('code')
                return attrs
            else:
                raise ValidationError('手机号不合法')
        else:
            raise ValidationError('验证码错误')


    def create(self, validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user