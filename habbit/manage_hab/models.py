from django.db import models
from users.models import User

class Habbit(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    name = models.CharField(max_length=300,verbose_name='Привычка')
    goal = models.SmallIntegerField(verbose_name='Цель')
    current_value = models.SmallIntegerField(verbose_name='Текущее значение')
    update_time = models.DateTimeField(auto_now=True)
    habbit_group = models.ForeignKey('HabbitGroup', on_delete=models.PROTECT, blank=True)


    def __str__(self):
        return self.name   



class HabbitProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь')
    habbit = models.ForeignKey(Habbit, on_delete=models.PROTECT, verbose_name='Привычка')
    current_value = models.SmallIntegerField(verbose_name='Текущее значение')
    update_time = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.user.username + self.habbit.name 
    
    

class HabbitGroup(models.Model):
    name = models.CharField(max_length=300,verbose_name='Название группы')


    def __str__(self):
        return self.name   
