from django.contrib import admin

from .models import LoginAction, LoginList


models = [LoginAction, LoginList]
admin.site.register(models)
