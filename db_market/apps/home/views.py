from django.shortcuts import render

from rest_framework.views import APIView
from db_market.utils.response import APIResponse
from db_market.utils.logger import log

from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from . import models
from . import serializer

# Create your views here.
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response
class SliderView(GenericViewSet, ListModelMixin):
    # 无论有多少条待展示的数据，最多就展示3条
    queryset = models.Slider.objects.filter(is_delete=False, is_show=True).order_by('orders')[
               :settings.SLIDER_COUNTER]
    serializer_class = serializer.SliderModelSerilaizer

    def list(self, request, *args, **kwargs):

        # response=super().list(request, *args, **kwargs)
        # 把data的数据加缓存
        # 1 先去缓存拿数据
        banner_list=cache.get('banner_list')
        if not banner_list:
            print('走数据库了')
            # 缓存中没有，去数据库拿
            response = super().list(request, *args, **kwargs)
            # 加到缓存
            cache.set('slider_list',response.data,60*60*24)
            return response

        return Response(data=slider_list)