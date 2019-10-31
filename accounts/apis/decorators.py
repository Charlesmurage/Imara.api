from rest_framework.response import Response
from rest_framework.views import status
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from accounts.models import CustomUser, Urban, Skills, Membership


def validate_signup_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        first_name = args[0].request.data.get("first_name", "")
        last_name = args[0].request.data.get("last_name", "")
        stage_name = args[0].request.data.get("stage_name", "")
        email = args[0].request.data.get("email", "")
        phone = args[0].request.data.get("phone", "")
        password = args[0].request.data.get("password", "")
        urban_centre = args[0].request.data.get("urban_centre", "")
        major_skill = args[0].request.data.get("major_skill", "")
        minor_skill = args[0].request.data.get("minor_skill", "")
        agree_to_license = args[0].request.data.get("agree_to_license", "")

        if not first_name:
            return Response(
                data={
                    "message": "first_name is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not last_name:
            return Response(
                data={
                    "message": "last_name is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not stage_name:
            return Response(
                data={
                    "message": "stage_name is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not email:
            return Response(
                data={
                    "message": "email is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not phone:
            return Response(
                data={
                    "message": "phone is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                data={
                    "message": "password is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not urban_centre:
            return Response(
                data={
                    "message": "urban_centre is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            ) 

        if not major_skill:
            return Response(
                data={
                    "message": "major_skill is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )   

        if not minor_skill:
            return Response(
                data={
                    "message": "minor_skill is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(urban_centre, int):
            return Response(
                data={
                    "message": "urban_centre should be of type integer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(major_skill, int):
            return Response(
                data={
                    "message": "major_skill should be of type integer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(minor_skill, int):
            return Response(
                data={
                    "message": "minor_skill should be of type integer"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError as e:
            return Response(
                data={
                    "error": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password, user=None, password_validators=None)
        except ValidationError as e:
            return Response(
                data={
                    "error": e
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not Urban.objects.filter(pk=urban_centre):
            return Response(
                data={
                    "error": "No urban centre with ID: {} found".format(urban_centre)
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not Skills.objects.filter(pk=major_skill):
            return Response(
                data={
                    "error": "No major skill with ID: {} found".format(major_skill)
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not Skills.objects.filter(pk=minor_skill):
            return Response(
                data={
                    "error": "No major skill with ID: {} found".format(minor_skill)
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if CustomUser.objects.filter(email = email):
            return Response(
                data={
                    "error": "A user with that email already exists"
                },
                status=status.HTTP_409_CONFLICT
            )

        if CustomUser.objects.filter(phone = phone):
            return Response(
                data={
                    "error": "A user with that phone number already exists"
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
        return fn(*args, **kwargs)
    return decorated

def validate_signin_data(fn):
    def decorated(*args, **kwargs):
        email = args[0].request.data.get("email", "")
        phone = args[0].request.data.get("phone", "")
        password = args[0].request.data.get("password", "")

        if (email and phone) or not(email or phone):
            return Response(
                data={
                    "message": "Please provide either a valid email or phone number"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                data={
                    "message": "Please provide a password"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return fn(*args, **kwargs)
    return decorated

def validate_update_profile_data(fn):
    def decorated(*args, **kwargs):
        image = args[0].request.data.get("image", "")
        first_name = args[0].request.data.get("first_name", "")
        last_name = args[0].request.data.get("last_name", "")
        stage_name = args[0].request.data.get("stage_name", "")
        email = args[0].request.data.get("email", "")
        phone = args[0].request.data.get("phone", "")
        bio = args[0].request.data.get("bio", "")
        urban_centre = args[0].request.data.get("urban_centre", "")
        major_skill = args[0].request.data.get("major_skill", "")
        minor_skill = args[0].request.data.get("minor_skill", "")

        condition = [image, first_name, last_name, stage_name, email, phone, bio, urban_centre, major_skill, minor_skill]

        if not any(condition):
            return Response(
                    data={
                        "message": "The parameter passed is invalid for this request"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return fn(*args, **kwargs)
    return decorated  

def validate_group_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        creator = args[0].request.data.get("creator", "")

        if Membership.objects.filter(creator = creator):
            return Response(
                data={
                    "error": "You are already in this group"
                },
                status=status.HTTP_409_CONFLICT
            )

        return fn(*args, **kwargs)
    return decorated

