from django.urls import path
from . import views

urlpatterns = [
    path("", views.test),
    path('bookings/', views.booking_list_create),
    path('bookings/<int:id>/', views.booking_detail),
    path('booking_verification/', views.update_booking_verification),
]
