
from rest_framework import serializers
from . import models


class SliderModelSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = models.Slider
        field = ['name', 'link', 'img']