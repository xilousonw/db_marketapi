from django.urls import path, re_path, include
from . import views

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('slider', views.SliderView, 'slider')
urlpatterns = [
    path('', include(router.urls)),

]