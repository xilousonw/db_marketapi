from django.db import models

# Create your models here.

from db_market.utils.models import BaseModel

class goods(BaseModel):
    title = models.CharField(max_length=128,verbose_name='商品标题')
    src = models.ImageField(upload_to='goods', default='goods/default.png',verbose_name='商品图片')
    url = models.CharField(max_length=64,verbose_name='商品跳转地址')
    newPrice = models.CharField(max_length=32,verbose_name='最新价格')
    oldPrice = models.CharField(max_length=32,verbose_name='原价')


    class Meta:
        db_table = 'market_goods'
        verbose_name = '集市商品'
        verbose_name_plural = '集市商品'

    def __str__(self):
        return '%s' % self.title


class goods_detail(BaseModel):
    desc = models.TextField(max_length=2048, verbose_name='商品详情')
    comment = models.CharField(max_length=128,verbose_name='用户评论')
    discuss = models.CharField(max_length=128,verbose_name='用户讨论')



class shop(BaseModel):
    icon = models.ImageField(upload_to='shops', default='shops/default.png',verbose_name='店铺图片')
    name = models.CharField(max_length=32,verbose_name='店铺名称')
    intro = models.CharField(max_length=128,verbose_name='店铺简介')
    url = models.CharField(max_length=128,verbose_name='店铺地址链接')

    goods = models.ManyToManyField(to=goods,on_delete=models.DO_NOTHING,db_constraint=False)


class comment(BaseModel):
    username = models.CharField(max_length=32,verbose_name='评论用户')
    usericon = models.ImageField(upload_to='icon', default='icon/default.png',verbose_name='用户头像')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    cmt_time = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 自关联
    parent = models.ForeignKey(to='self', null=True)  # 有些评论就是根评

    goods = models.ForeignKey(to='goods',on_delete=models.CASCADE)


class discuss(BaseModel):
    username = models.CharField(max_length=32,verbose_name='讨论用户')
    usericon = models.ImageField(upload_to='icon', default='icon/default.png',verbose_name='用户头像')
    content = models.CharField(verbose_name='讨论内容', max_length=255)
    dis_time = models.DateTimeField(auto_now_add=True, verbose_name='讨论时间')

    goods = models.ForeignKey(to='goods',on_delete=models.CASCADE)