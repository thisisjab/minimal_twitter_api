from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'users/activate/<uid>/<token>',
        views.UserActivateView.as_view(),
        name='user-activate',
    ),
    path(
        'users/request-activation-email/',
        views.UserRequestActivationEmailView.as_view(),
        name='user-request-activation-email',
    ),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
