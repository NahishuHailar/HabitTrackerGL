from rest_framework import serializers
from users.models import User, UserAvatar
from manage_hab.models import (
    Habit, 
    HabitGroup, 
    HabitProgress, 
    Icon
    )


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firebase_key', 'auth_type', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        ref_name = 'CustomUserModelSerialize'

    def to_representation(self, instance):
        rep = super(UserSerializer, self).to_representation(instance)
        if instance.avatar:
            rep['avatar'] = instance.avatar.title
        return rep
    
    def to_internal_value(self, data):
            data_copy = data.copy()
            user_avatar_title = data_copy.get('avatar', None)
            if user_avatar_title:
                try:
                    user_avatar_id = UserAvatar.objects.get(title=user_avatar_title).id
                    data_copy['avatar'] = user_avatar_id
                except UserAvatar.DoesNotExist:
                    raise serializers.ValidationError("UserAvatar does not exist.")
            return super().to_internal_value(data_copy)
    


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(HabitSerializer, self).to_representation(instance)
        if instance.habit_group:
            rep['habit_group'] = instance.habit_group.name
        return rep
    
    def to_internal_value(self, data):
            data_copy = data.copy()
            habit_group_name = data_copy.get('habit_group')
            if habit_group_name:
                try:
                    habit_group_id = HabitGroup.objects.get(name=habit_group_name).id
                    data_copy['habit_group'] = habit_group_id
                except HabitGroup.DoesNotExist:
                    raise serializers.ValidationError("Habit group does not exist.")
            return super().to_internal_value(data_copy)


class HabitDatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitProgress
        fields = "__all__"


class HabitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitGroup()
        fields = "__all__"

class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAvatar
        fields = "__all__"
    
    def to_representation(self, instance):
        rep = super(AvatarSerializer, self).to_representation(instance)
        if instance.avatar_group:
            rep['avatar_group'] = instance.avatar_group.name
        return rep    

class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(IconSerializer, self).to_representation(instance)
        rep['habit_group'] = instance.habit_group.name
        return rep
