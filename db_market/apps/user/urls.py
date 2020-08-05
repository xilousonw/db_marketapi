from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', views.LoginView, 'login')
router.register('', views.SendSmSView, 'send')
router.register('register', views.RegisterView, 'register')  # /user/register   post请求就是新增
urlpatterns = [
    path('', include(router.urls)),


]