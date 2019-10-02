from django.urls import path, include
from accounts.apis.views import (
    UserListView, CreatorView
)

app_name = "accounts"

urlpatterns = [
    path('users/', UserListView.as_view(), name="list"),
    path('creators/', CreatorView.as_view(), name="creator-register"),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]