from django.urls import path, include
from accounts.apis.views import (
    UserListView,
)

app_name = "accounts"

urlpatterns = [
    path('users/', UserListView.as_view(), name="list"),
    path('rest-auth/', include('rest_auth.urls')),
]