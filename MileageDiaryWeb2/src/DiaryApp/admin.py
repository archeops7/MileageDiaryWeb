
# Register your models here.
from django.contrib import admin

from .models import Log

class LogAdmin(admin.ModelAdmin):
    list_display = ('id','trip_memo', 'km', 'litter', 'updated_at')
    list_display_links = ('id', 'trip_memo')
    
admin.site.register(Log, LogAdmin)