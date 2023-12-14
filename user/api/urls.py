from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from user.api import views
from user.api.views import RegisterUserAPIView, UpdateProfileView, LogoutView, ObtainTokenView

urlpatterns = [
    path('token/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customers/', RegisterUserAPIView.as_view()),
    path('customers/<int:pk>/', UpdateProfileView.as_view(), name='update_profile'),
    path('logout/', LogoutView.as_view(), name='logout')
]
