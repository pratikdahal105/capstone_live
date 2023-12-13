from django.urls import path
from . import views

urlpatterns = [
    path("", views.test),
    path('users/', views.user_list_create),
    path('users/<int:id>/', views.user_detail),
    path('events/', views.event_list_create),
    path('events/<int:id>/', views.event_detail),
    path('bookings/', views.booking_list_create, name='booking-list-create'),
    path('bookings/<int:id>/', views.booking_detail, name='booking-detail'),
]
