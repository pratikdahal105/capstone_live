from django.urls import path
from . import views

urlpatterns = [
    path("", views.test),
    path('sponsors/', views.sponsor_list_create),
    path('sponsors/<slug:slug>/', views.sponsor_detail),

]
