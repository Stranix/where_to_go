from django.urls import path

from places import views

urlpatterns = [
    path('<int:pk>/', views.show_place, name='show-place'),
]
