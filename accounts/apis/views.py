from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from accounts.models import CustomUser, Creator, Group, Membership
from accounts.apis.serializers import UserSerializer, CreatorSerializer, GroupSerializer, MembershipSerializer

class UserListView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class CreatorView(generics.ListCreateAPIView):
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer

    def load_urban(request):
        county_id = request.GET.get('county')
        urban = Urban.objects.filter(county_id=county_id).order_by('county')

class CreatorPartialUpdateView(GenericAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    fields = ('first_name', 'last_name')

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class MembershipView(generics.ListCreateAPIView):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer