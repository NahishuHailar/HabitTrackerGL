from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from .models import HabbitGroup, Habbit, HabbitProgress

@admin.register(Habbit)
class HabbitAdmin(admin.ModelAdmin):
    fields = ['user', 'name', 'goal', 'current_value', 'habbit_group']
    list_display = ('id', 'user', 'name',  'goal', 'current_value', 'habbit_group', 'update_time')

    

@admin.register(HabbitGroup)
class HabbitGroupAdmin(admin.ModelAdmin):
    fields = ['name',]
    list_display = ('id', 'name',)
    

    

@admin.register(HabbitProgress)
class HabbitProgressAdmin(admin.ModelAdmin):
    fields = ['user', 'habbit', 'current_value']
    list_display = ('id', 'user','habbit', 'current_value', 'update_time')
    


