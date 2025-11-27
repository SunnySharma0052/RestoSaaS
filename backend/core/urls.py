"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from payments.views import CreatePaymentAPI
from django.conf import settings
from django.conf.urls.static import static

# Views import
from orders.views import CreateOrderAPI, StaffOrderListAPI, UpdateOrderStatusAPI # Naye views import kiye
from rest_framework.authtoken.views import obtain_auth_token # Import karein
from analytics.views import SubmitReviewAPI, ManagerStatsAPI # <--- Ye Import Zaroori hai
from menu.views import RestaurantMenuAPI, RestaurantMenuAPI, ManagerMenuItemsAPI, UpdateItemAPI # Import update karein

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Login API
    path('api/login/', obtain_auth_token, name='api_token_auth'),

    # Guest APIs
    path('api/menu/<slug:restaurant_slug>/', RestaurantMenuAPI.as_view()),
    path('api/order/create/', CreateOrderAPI.as_view()),
    path('api/payment/create/', CreatePaymentAPI.as_view()),
    path('api/review/submit/', SubmitReviewAPI.as_view()),

    # Staff/Kitchen APIs
    path('api/staff/orders/<int:restaurant_id>/', StaffOrderListAPI.as_view()),
    path('api/staff/order/<int:pk>/update/', UpdateOrderStatusAPI.as_view()),

    # Manager API (Ye line missing thi ya galat thi)
    path('api/manager/stats/<int:restaurant_id>/', ManagerStatsAPI.as_view()),

    # Manager Menu APIs
    path('api/manager/menu/<int:restaurant_id>/', ManagerMenuItemsAPI.as_view()),
    path('api/manager/item/<int:pk>/update/', UpdateItemAPI.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)