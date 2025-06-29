"""
URL configuration for antonella_back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .settings import BASE_DIR
import os

urlpatterns = [
    path('api/', include('app.user.urls')),
    path('api/store_service/', include('app.store_service.urls')),
    path('api/token/', include('app.tokens.urls')),
    path('api/product/', include('app.product.urls')),
    path('api/config/', include('app.config.urls')),
    path('api/payment/', include('app.payment.urls')),
    path('api/order/', include('app.order.urls')),
    path('api/answer/', include('app.answers.urls')),
    path('api/publicidad/', include('app.publicidad.urls')),
    path('api/chat/', include('app.chat.urls')),
    re_path(r'^admin(?:/.*)?$', TemplateView.as_view(template_name='index.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, "client", "dist", "assets"))
