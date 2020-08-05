from django.db import models

# Create your models here.
from db_market.utils.models import BaseModel


class Slider(BaseModel):
    name = models.CharField(max_length=32,verbose_name='图片名字')
    img = models.ImageField(upload_to='slider', verbose_name='轮播图', null=True)
    link = models.CharField(max_length=32,verbose_name='跳转链接')
    info = models.TextField(verbose_name='图片简介')


    def  __str__(self):
        return self.name

