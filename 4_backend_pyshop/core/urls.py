from django.contrib import admin
from django.urls import path, include
from checks.views import create_order

urlpatterns = [
    path('admin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
    path('api/create_order/', create_order),
]