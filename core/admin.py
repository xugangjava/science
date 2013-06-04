#coding=utf-8
from django.contrib import admin
from models import Models

for m in Models: admin.site.register(m)

