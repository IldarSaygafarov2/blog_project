from django.urls import path

from . import views

# http://127.0.0.1:8000/
# http://127.0.0.1:8000/users/login/

urlpatterns = [
    path('login/', views.login_user, name='login-user'),
    path('registration/', views.register_user, name='register-user'),
    path('logout/', views.logout_user, name='logout-user'),
    path('profile/<str:username>', views.profile_page, name='profile')
]