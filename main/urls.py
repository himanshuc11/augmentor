from django.urls import path
from .views import SignUpView, CRUDView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('crud/', CRUDView.as_view()),
]
