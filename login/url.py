from django.urls import path
from .views import UserLogin,UserRegister,UserLogout

urlpatterns = [
    path('', UserRegister.as_view(), name='registerapi'),
    path('loginapi/', UserLogin.as_view(), name='loginapi'),
    path('logoutapi/',UserLogout.as_view(),name='logoutapi')
]

