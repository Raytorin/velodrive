"""
URL configuration for velodrive_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from bike_app.views import ReturnBikeView, RentalHistoryView, RentBikeView, BikesListCreateView, AvailableBikesListView
from bike_app.views import RentalHistoryView, BikesListCreateView, AvailableBikesListView, BikeRentalViewSet
from main_app.views import UserCreateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/bike/rental', BikeRentalViewSet, basename='rental')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/register/', UserCreateView.as_view(), name="register"),
    path('api/users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/bikes/available/', AvailableBikesListView.as_view(), name='available_bikes'),
    path('api/bikes/register/', BikesListCreateView.as_view(), name='bikes_list_register'),
    path('', include(router.urls)),
    path('api/bikes/history/', RentalHistoryView.as_view(), name='rental_history'),
]
