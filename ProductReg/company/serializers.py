from django.urls import path, include
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()
from . models import *
from rest_framework import generics, permissions, serializers
from django.contrib.auth.hashers import make_password, check_password
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class RdbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rdb
        fields = ['company_name','tin_number']