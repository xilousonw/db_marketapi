from django.db import models
# 后期课程表，轮播图表，都会用到这些字段

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    is_show = models.BooleanField(default=True, verbose_name='是否展示')
    # 修改成这样
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time  = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    orders = models.IntegerField()
    class Meta:
        abstract=True  # 一定不要忘了


