from django.urls import path
from Medicine import views


urlpatterns = [
    path('medicine', views.MedicineView.as_view()),
]
