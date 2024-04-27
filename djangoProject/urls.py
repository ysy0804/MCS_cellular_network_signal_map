"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from app import views
from app.views import map_view




urlpatterns = [
    path('admin/', admin.site.urls),
    path('Map/', views.map_view),
    # path('process_request/', views.process_request),
    path('receive_data/', views.receive_data),
    path('get_latest_locations/', views.get_latest_locations),
    path('get_operator_Data/', views.get_operator_Data),
]
