from django.urls import path
from autoservice import api_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('get_all_users/', api_views.GetAllUsers.as_view()),
    path('get_user_cars/', api_views.GetUserCars.as_view()),
    path('get_user_data/', api_views.GetUserData.as_view()),
    path('change_user_data/', api_views.ChangUserData.as_view()),
    path('register_user/', api_views.RegisterUser.as_view()),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
