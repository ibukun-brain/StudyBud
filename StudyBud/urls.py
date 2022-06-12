"""StudyBud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, 
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView,
)


urlpatterns = [
    path('', include("base.urls", namespace='base')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('password-reset/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change-done', PasswordChangeDoneView.as_view(), name='password_change_done')


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)