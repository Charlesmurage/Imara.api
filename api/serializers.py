from rest_framework import serializers
from api.models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserProfile
        fields = ('stage_name', 'phone', 'county', 'urban_centre', 'major_skill', 'minor_skill', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.stage_name = profile_data.get('stage_name', profile.stage_name)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.county = profile_data.get('county', profile.county)
        profile.urban_centre = profile_data.get('urban_centre', profile.urban_centre)
        profile.major_skill = profile_data.get('major_skill', profile.major_skill)
        profile.minor_skill = profile_data.get('minor_skill', profile.minor_skill)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance