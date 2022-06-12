from django.urls import path
from .views import CustomLoginView, SignUpView, user_profile, user_settings
from django.contrib.auth.views import LogoutView

app_name = 'accounts'


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>', user_profile, name='user-profile'),
    path('user-settings/', user_settings, name='user-settings'),


]
