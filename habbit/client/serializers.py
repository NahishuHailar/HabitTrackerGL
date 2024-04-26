from rest_framework import serializers
from users.models import User 
from manage_hab.models import Habbit, HabbitGroup
 
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'image')


class HabbitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habbit  
        fields = '__all__'      

class HabbitSerializerdates(serializers.ModelSerializer):
    class Meta:
        model = Habbit  
        fields = ('update_time',)              


class HabbitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabbitGroup()  
        fields = ('name',)                      