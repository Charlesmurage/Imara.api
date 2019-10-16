from rest_framework import serializers
from accounts.models import CustomUser, Creator, Group, Membership, Counties, Urban, Skills
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

class CreatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Creator
        fields = ('first_name', 'last_name','stage_name', 'email', 'phone', 'password', 'urban_centre', 'major_skill', 'minor_skill', 'agree_to_license')

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

    def delete(self, request, pk):
        group = get_object_or_404(Group.objects.all(), pk=pk)
        group.delete()
        
        return Response({"message":"Group with id '{}' has been deleted.".format(pk)},status=204)

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ('creator', 'group')

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class CountySerializer(serializers.ModelSerializer):
    class Meta:
        model = Counties
        fields = '__all__'

class UrbanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urban
        fields = '__all__'

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

