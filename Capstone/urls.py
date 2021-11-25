"""Capstone URL Configuration

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
from django.urls import path, include
from django.conf.urls import url
from markdownx import urls as markdownx
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kapchikachi.urls', namespace="kapchikachi")),
    path('markdownx/', include('markdownx.urls')),
    path('common/', include('common.urls', namespace="common")),
    # path('', include('kapchikachi.urls')), #입력 안하면 자동으로 kapchokachi로 이동

    #소셜로그인 기능
    path('accounts/', include('allauth.urls')),

    #정적파일처리
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
