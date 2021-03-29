from django.urls import path
from Lab import views
# from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('home', views.home),
    path('lab/notsure', views.NotSureView.as_view()),
    path('lab/data', views.GetTestView.as_view()),
    path('lab/add-to-cart',views.add_to_cart.as_view()),
    path('lab/remove-from-cart',views.remove_from_cart.as_view()),
    path('lab/cart',views.CartView.as_view()),
    path('lab/order',views.OrderView.as_view()),
    path('lab/address',views.AddressView.as_view()),
    path('lab/place',views.PlaceOrderAPI.as_view()),


    path('lab/<str:type>/<int:pk>',views.TestAPI.as_view()),
    # path('lab/test/1',views.TestView),
    path('hlthpkgdetails/<int:id>',views.hlthpkgprofile),
    path('testdetails/<int:id>',views.testprofile),

]
