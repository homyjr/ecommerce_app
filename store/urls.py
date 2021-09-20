from django.urls import path
from . import views

urlpatterns = [path('', views.products_display, name = 'displayproducts'),
               path('addtocart/', views.add_to_cart, name = 'addtocart'),
               path('cart/', views.cart, name = 'cart'),
               path('updatecart/', views.updatecart, name='updatecart'),
               path('login/', views.loginUser, name="login"),
               path('logout/', views.logoutUser, name="logout"),
               path('register/', views.registerUser, name="register"),
               path('shipping/',views.shippingaddress, name='shipping'),
               path('payment/', views.payment, name = 'payment'),
               path('myorder/', views.myorder, name='myorder'),
               path('ordersuccess/<uuid:id>', views.ordersuccess, name = 'ordersuccess'),
               path('cancelorder/<int:id>', views.cancelorder, name= 'cancelorder'),
               path('categories/<int:id>', views.products_display, name='categories'),
               path('search/',views.search, name = 'search'),
               path('productdetails/<int:id>' ,views.ShowProductDetailsAndReviews, name='productdetails'),
               path('buynow/<int:id>' ,views.buynow, name='buynow'),
               path('writereview/', views.writereview, name='writereview'),
               path('increasereviews/', views.IncreaseReviews, name='IncreaseReviews'),
               path('myaccount/', views.myaccount, name='myaccount')]