from django.contrib import admin
from django.urls import path,include
from .views import RegisterUserView,LoginUserView,RegisterMessView, LoginMessView

urlpatterns = [
    path('user-register/',RegisterUserView.as_view()),
    path('user-login/',LoginUserView.as_view()),
    path('mess-login/',LoginMessView.as_view()),
    path('mess-register/',RegisterMessView.as_view())
]