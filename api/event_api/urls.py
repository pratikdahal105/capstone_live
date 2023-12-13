from django.urls import path
from . import views

urlpatterns = [
    path("", views.test),
    path('events/', views.event_list_create),
    path('events/<slug:slug>/', views.event_detail),
    path('events/<slug:event_slug>/add_user/', views.add_user_to_event),
    path('dashboard/', views.dasboard_details),
]
