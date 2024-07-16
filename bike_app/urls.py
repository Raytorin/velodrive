from django.urls import path
from .views import AvailableBikesListView, RentBikeView, ReturnBikeView, RentalHistoryView

urlpatterns = [
    path('available/', AvailableBikesListView.as_view(), name='available_bikes'),
    path('rent/', ReturnBikeView.as_view(), name='rent_bike'),
    path('return/<int:pk>/', ReturnBikeView.as_view(), name='return_bike'),
    path('history/', RentalHistoryView.as_view(), name='rental_history'),
]
