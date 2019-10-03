from django.urls import path, include
from accounts.apis.views import (
    UserListView, CreatorView, CreatorPartialUpdateView
)

app_name = "accounts"

urlpatterns = [
    path('users/', UserListView.as_view(), name="list"),
    path('creators/', CreatorView.as_view(), name="creator-register"),
    path('creators/update-partial/<int:pk>/', CreatorPartialUpdateView.as_view(), name='creator_partial_update'),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]