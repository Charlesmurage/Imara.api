from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from accounts.models import CustomUser, Creator, Group, Membership, Counties, Urban, Major, Minor
from accounts.apis.serializers import UserSerializer, CreatorSerializer, GroupSerializer, MembershipSerializer, TokenSerializer, UserLoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


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
        county = int(request.data.get("county", ""))
        urban_centre = int(request.data.get("urban_centre", ""))
        major_skill = int(request.data.get("major_skill", ""))
        minor_skill = int(request.data.get("minor_skill", ""))
        agree_to_license = request.data.get("agree_to_license", "")
        if not first_name and not last_name and not stage_name and not password and not email:
            return Response(
                data={
                    "message": "Please fill in all required fields"
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
        first_name=first_name, last_name=last_name, stage_name=stage_name, email=email, phone=phone, password=password, county=Counties.objects.filter(county), urban_centre= Urban.objects.filter(urban_centre), major_skill=Major.objects.filter(major_skill), minor_skill=Minor.objects.filter(minor_skill), agree_to_license=agree_to_license 
        )
        return Response(
            data=CreatorSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )        


class CreatorPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
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


class MembershipView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
