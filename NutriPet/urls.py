"""
URL configuration for NutriPet project.

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
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from recomendador import views
from .api_views import RecomendacionViewSet

router = DefaultRouter()
router.register(r'recomendaciones', RecomendacionViewSet, basename='recomendacion')

urlpatterns = [
    path('', lambda request: redirect('login'), name='index'),  # Redirección en la raíz
    path('admin/', admin.site.urls),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('registros/', views.lista, name='lista'),
    path('registros/crear/', views.crear, name='crear'),
    path('registros/<int:pk>/editar/', views.editar, name='editar'),
    path('registros/<int:pk>/eliminar/', views.eliminar, name='eliminar'),
    path('api/token/', obtain_auth_token, name='api-token'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/', include(router.urls)),
]