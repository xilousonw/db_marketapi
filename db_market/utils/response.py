
from rest_framework.response import  Response


class APIResponse(Response):
    def __init__(self,code=1,msg='成功',result=None,status=None,headers=None,content_type=None,**kwargs):
        dic={
            'code':code,
            'msg':msg

             }
        if result:
            dic['result']=result
        dic.update(kwargs)

        #对象来调用对象的绑定方法，会自动传值
        super().__init__(data=dic,status=status,headers=headers,content_type=content_type)

        # 类来调用对象的绑定方法，这个方法就是一个普通函数，有几个参数就要传几个参数
        # Response.__init__(data=dic,status=status,headers=headers,content_type=content_type)