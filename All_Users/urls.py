from django.urls import path
from All_Users import views
from knox.views import LogoutView
from django.contrib import admin
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('send_otp', views.send_otp.as_view()),
    path('verify_user', views.verify_user.as_view()),
    path('Register', views.Register.as_view()),

    path('login', views.LoginAPI.as_view()),
    path('logout', LogoutView.as_view()),
    path('profile', views.ProfileView.as_view()),
    # path('updateprofile', views.UpdateProfileView.as_view()),
      path('',RedirectView.as_view(url="home")),
    path('signup/', views.signup),
    path('signin/', views.signin),

    path("contact/", views.contact, name="contact"),
    path("tests/", views.tests, name="tests"),
    path("healthpackages/", views.hlthpkg, name="teshealthpackagests"),
    path("about/", views.about, name="about"),
    path("joinus/", views.joinus, name="joinus"),
    path("cart/", views.cart, name="cart"),



    path("ordermedicines/", views.medicine, name="ordermedicine"),
    path("ordersummary/", views.ordersum, name="ordersummary"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("checkout/", views.checkout, name="checkout"),
    path("bookdoctor/", views.bookdoctor, name="bookdoctor"),
    path("conditions/", views.conditions, name="conditions"),
    path("specializations/", views.specializations, name="specializations"),
]
