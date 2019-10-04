from rest_framework import serializers
from accounts.models import CustomUser, Creator
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', )

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ('username', 'first_name', 'last_name', 'email', "password",'county','urban_centre','major_skill','minor_skill')

    validate_password = make_password


    def partial_update(self, instance,  validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance
