from django.urls import path
from .views import SignUpView, CRUDView, LoginAPIView, LogoutAPIView, CompanyView

urlpatterns = [
    path('', SignUpView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('crud/', CRUDView.as_view()),
    path('data/<str:company_name>', CompanyView.as_view())
]
