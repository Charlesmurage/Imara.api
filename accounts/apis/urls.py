from django.urls import path, include
from accounts.apis.views import (
    UsersListView, CreatorPartialUpdateView, GroupView, MembershipView, CreatorSignupView, UserLoginView
)
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    # URLs related to all users

    path('users/', UsersListView.as_view(), name="list_all_users"),
    path('signin/', UserLoginView.as_view(), name="user_login"),

    # URLs related to Content Creators
    path('creators/signup/', CreatorSignupView.as_view(), name="creator_signup"),
    path('creators/update-partial/<int:pk>/', CreatorPartialUpdateView.as_view(), name='creator_update_profile'),
    path('creators/group/', GroupView.as_view(), name="groups"),
    path('creators/members/', MembershipView.as_view(), name="members"),
    #path('password/reset/', auth_views.PasswordResetView.as_view()),
]