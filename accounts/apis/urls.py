from django.urls import path, include
from accounts.apis.views import (
    UsersListView, CreatorDetailView, GroupPartialUpdateView, GroupView, GroupByIdView, MembershipView, CreatorSignupView, UserLoginView, CountiesView, UrbanCentresView, SkillsView
)
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path('counties/', CountiesView.as_view(), name="list_all_counties"),
    path('urbancentres/', UrbanCentresView.as_view(), name="list_all_urban_centers"),
    path('skills/', SkillsView.as_view(), name="list_all_skills"),
    # path('minorskills/', MinorSkillsView.as_view(), name="list_all_minorskills"),
    # URLs related to all users

    path('users/', UsersListView.as_view(), name="list_all_users"),
    path('signin/', UserLoginView.as_view(), name="user_login"),

    # URLs related to Content Creators
    path('creators/signup/', CreatorSignupView.as_view(), name="creator_signup"),
    path('creators/<int:pk>/', CreatorDetailView.as_view(), name='creator_update_profile'),
    path('creators/group/update-partial/<int:pk>/', GroupPartialUpdateView.as_view(), name='update_group'),
    path('creators/group/delete/<int:pk>/', GroupView.as_view(), name='delete_group'),
    path('creators/members/delete/<int:pk>/', MembershipView.as_view(), name='delete_member'),
    path('creators/<int:pk>/', CreatorView.as_view(), name='creator_profile'),
    path('creators/groups/', GroupView.as_view(), name="groups"),
    path('creators/groups/<int:pk>/', GroupByIdView.as_view(), name="get_group_by_id"),
    path('creators/members/', MembershipView.as_view(), name="members"),
    #path('password/reset/', auth_views.PasswordResetView.as_view()),
    path('rest-auth/', include('rest_auth.urls'))
]