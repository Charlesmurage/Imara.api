from rest_framework.response import Response
from rest_framework.views import status
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from accounts.models import CustomUser, Urban, Skills


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

        if not first_name or not last_name or not stage_name or not password or not email or not phone or not password or not urban_centre or not major_skill or not minor_skill:
            return Response(
                data={
                    "message": "Please fill in all the fields"
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

        if agree_to_license != True:
            return Response(
                data={
                    "message": "You have to agree to the Creator license"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated