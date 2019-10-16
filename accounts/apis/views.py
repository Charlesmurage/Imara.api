from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from accounts.models import CustomUser, Creator, Group, Membership, Counties, Urban, Skills
from accounts.apis.serializers import UserSerializer, CreatorSerializer, GroupSerializer, MembershipSerializer, TokenSerializer, UserLoginSerializer, CountySerializer, UrbanSerializer, SkillsSerializer
from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.shortcuts import get_object_or_404




# Classes related to all users on the system


class UsersListView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class UserLoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(
                data={
                    "message": "Wrong email or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


# Classes related to all Creators in the system


class CreatorSignupView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreatorSerializer

    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")
        stage_name = request.data.get("stage_name", "")
        email = request.data.get("email", "")
        phone = request.data.get("phone", "")
        password = request.data.get("password", "")
        county = request.data.get("county", "")
        urban_centre = request.data.get("urban_centre", "")
        major_skill = request.data.get("major_skill", "")
        minor_skill = request.data.get("minor_skill", "")
        agree_to_license = request.data.get("agree_to_license", "")
        if not first_name and not last_name and not stage_name and not password and not email:
            return Response(
                data={
                    "message": "Please fill in all required fields"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if county == "" and urban_centre == "" and major_skill == "" and minor_skill == "":
            return Response(
                data={
                    "message": "Provide county and major skills details"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if CustomUser.objects.filter(email = email):
            return Response(
                data={
                    "message": "A user with that email already exists"
                },
                status=status.HTTP_409_CONFLICT
            )
        if agree_to_license != True:
            return Response(
                data={
                    "message": "You have to agree to the Creator license"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = Creator.objects.create_user(
        first_name=first_name, last_name=last_name, stage_name=stage_name, email=email, phone=phone, password=password, urban_centre= get_object_or_404(Urban, pk=int(urban_centre)), major_skill=get_object_or_404(Skills, pk=int(major_skill)), minor_skill=get_object_or_404(Skills, pk=int(minor_skill)), agree_to_license=agree_to_license 
        )
        return Response(
            data=CreatorSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )        


class CreatorPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    permission_classes = (permissions.IsAuthenticated,)


    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    fields = ('first_name', 'last_name')

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


# Classes related to all groups in the system

class GroupView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


    def delete(self, request, pk):
        group = get_object_or_404(Group.objects.all(), pk=pk)
        group.delete()
        
        return Response({"message":"Group with id '{}' has been deleted.".format(pk)},status=204)


class MembershipView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    


class CountiesView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Counties.objects.all()
    serializer_class = CountySerializer

class UrbanCentresView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Urban.objects.all()
    serializer_class = UrbanSerializer

class SkillsView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


