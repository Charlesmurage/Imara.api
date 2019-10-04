from rest_framework import serializers
from accounts.models import CustomUser, Creator, Group, Membership
from django.contrib.auth.hashers import make_password
from drf_writable_nested import WritableNestedModelSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', )

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ('username', 'first_name', 'last_name','stage_name', 'email', "password",'county','urban_centre','major_skill','minor_skill')

    validate_password = make_password


    def partial_update(self, instance,  validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', 'members', )

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('creator', 'group', 'date_joined', 'invite_reason' )