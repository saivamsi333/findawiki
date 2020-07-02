from .models import *
from rest_framework import serializers

class WikiSerializer(serializers.ModelSerializer):
    class Meta:
        model=Wiki
        fields='__all__'
