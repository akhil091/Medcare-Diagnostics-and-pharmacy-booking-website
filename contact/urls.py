from django.urls import path
from contact import views


urlpatterns = [
    path('contactus', views.ContactView.as_view()),
]
