"""
URL configuration for librarymanagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from library import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
# from .views import CustomTokenObtainPairView
from rest_framework.permissions import AllowAny
from django.urls import path


schema_view = get_schema_view(
    openapi.Info(
        title="Book API",
        default_version='v1',
        description="API for managing books",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("admin/", admin.site.urls),
    path('create-user/', views.CreateUserView.as_view(), name='create_user'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='custom_login'),
    path('books/', views.BookList.as_view(), name='book-list'),         # List and create
    path('books/<int:pk>/', views.BookDetail.as_view(), name='book-detail'),
    path('borrow-history/', views.ViewPersonalBorrowHistory.as_view(), name='view-personal-borrow-history'),
    path('download-history/', views.DownloadBorrowHistory.as_view(), name='download-borrow-history'),
    path('borrow-requests/', views.ViewBorrowRequests.as_view(), name='borrow-requests'),
]