orfrom rest_framework import generics

from accounts.models import CustomUser, Creator
from accounts.apis.serializers import UserSerializer, CreatorSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CreatorView(generics.ListCreateAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
