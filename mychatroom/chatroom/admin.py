from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone','name','email','sex','c_time']
    search_fields = ['phone','name']
admin.site.register(User,UserAdmin)

class UnreadMessageAdmin(admin.ModelAdmin):
    list_display = ['phone','sender','message','c_time']
    search_fields = ['phone','message']
admin.site.register(UnreadMessage,UnreadMessageAdmin)

class HistoricalMessageAdmin(admin.ModelAdmin):
    list_display = ['sender','message','c_time']
    search_fields = ['message']
admin.site.register(HistoricalMessage,HistoricalMessageAdmin)