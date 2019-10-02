from rest_framework import generics

from accounts.models import CustomUser
from accounts.apis.serializers import UserSerializer

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer