from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from accounts.models import CustomUser, Creator, Group, Membership, Counties, Urban, Skills
from accounts.apis.serializers import (
    UserSerializer, 
    CreatorSerializer, 
    CreatorProfileSerializer, 
    GroupSerializer, 
    MembershipSerializer, 
    TokenSerializer, 
    UserLoginSerializer, 
    CountySerializer, 
    UrbanSerializer, 
    SkillsSerializer,
    CreatorUpdateSerializer
)
from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from rest_framework.views import APIView
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.shortcuts import get_object_or_404
from .decorators import validate_signup_data, validate_signin_data, validate_update_profile_data, validate_group_data
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ObjectDoesNotExist


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
    queryset = Creator.objects.all()

    @validate_signin_data
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")

        try:
            email = CustomUser.objects.get(phone=phone).email
        except CustomUser.DoesNotExist:
            email = request.data.get("email")

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
            return Response(
                data={
                    "token": serializer.data['token'],
                    "id": user.id,
                    "firstName": user.first_name,
                    "lastName": user.last_name,
                    "email": user.email,
                    "password": user.password,
                    "isActive": user.is_active,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "last_login": user.last_login,
                    "date_joined": user.date_joined
                },
                status=status.HTTP_200_OK
            )
        return Response(
                data={
                    "message": "Wrong email or password"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):

    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        logout(request)

        return Response(
                data={
                    "success": "Successfully logged out."
                },
                status=status.HTTP_200_OK
            )

# Classes related to all Creators in the system


class CreatorSignupView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreatorSerializer

    @validate_signup_data
    def post(self, request, *args, **kwargs):
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        stage_name = request.data.get("stage_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        password = request.data.get("password")
        urban_centre = request.data.get("urban_centre")
        major_skill = request.data.get("major_skill")
        minor_skill = request.data.get("minor_skill")
        agree_to_license = request.data.get("agree_to_license")

        new_user = Creator.objects.create_user(
        first_name=first_name, last_name=last_name, stage_name=stage_name, email=email, phone=phone, password=password, urban_centre= get_object_or_404(Urban, pk=urban_centre), major_skill=get_object_or_404(Skills, pk=major_skill), minor_skill=get_object_or_404(Skills, pk=minor_skill), agree_to_license=agree_to_license 
        )
        return Response(
            data=CreatorSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )        


class CreatorDetailView(generics.RetrieveUpdateAPIView):
    '''
    GET /api/v1/accounts/creators/{id}
    PATCH /api/v1/accounts/creators/{id}
    '''
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)
    queryset = Creator.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            creator = self.queryset.get(pk=kwargs["pk"])
            if creator.id != request.user.id:
                return Response(
                    data={
                        "message": "You do not have the required permissions"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response(CreatorProfileSerializer(creator).data)
        except Creator.DoesNotExist:
            return Response(
                data={
                    "message": "Creator with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_update_profile_data
    def patch(self, request, *args, **kwargs):
        try:
            creator = self.queryset.get(pk=kwargs["pk"])
            if creator.id != request.user.id:
                return Response(
                    data={
                        "message": "You do not have the required permissions"
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            serializer = CreatorUpdateSerializer(creator, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                creator = serializer.save()                
                return Response(CreatorUpdateSerializer(creator).data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Creator.DoesNotExist:
            return Response(
                data={
                    "message": "Creator with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GroupPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    permission_classes = (permissions.IsAuthenticated,)


    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    fields = ('name')

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        return self.partial_update(request, *args, **kwargs)
    
    def pre_save(self, request, obj):
        obj.creator = request.user

class GroupByIdView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    def get(self, request, *args, **kwargs):
        try:
            group = self.queryset.get(pk=kwargs["pk"])
            return Response(GroupSerializer(group).data)
        except Group.DoesNotExist:
            return Response(
                data={
                    "message": "Group with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class GroupView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    
    


    def delete(self, request, pk):
        group = get_object_or_404(Group.objects.all(), pk=pk)
        group.delete()
        
        return Response({"message":"Group with id '{}' has been deleted.".format(pk)},status=204)


class MembershipView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

    # @validate_group_data
    # def post(self, request, *args, **kwargs):
    #     creator = request.data.get("creator")

    #     new_member = Membership.objects.create(
    #         creator = creator
    #     )

    #     return Response(
    #         data=GroupSerializer(new_member).data,
    #         status=status.HTTP_201_CREATED
    #     )    

    def delete(self, request, pk):
        member = get_object_or_404(Membership.objects.all(), pk=pk)
        member.delete()
        
        return Response({"message":"Member with id '{}' has been deleted.".format(pk)},status=204)

    


class CountiesView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Counties.objects.all()
    serializer_class = CountySerializer

class UrbanCentresView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UrbanSerializer

    def get_queryset(self):
        queryset = Urban.objects.all()
        county = self.request.query_params.get('county', '')
        if county:
            countyId = int(county)
            return queryset.filter(county=countyId)
        return queryset




class SkillsView(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


