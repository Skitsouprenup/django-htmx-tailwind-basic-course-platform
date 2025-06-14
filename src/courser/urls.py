"""
URL configuration for courser project.

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

from django.conf import settings
from django.conf.urls.static import static

from emails import views as email_views

from . import views

urlpatterns = [
    path("", views.home),
    # HTMX #
    path("login/", email_views.email_token_login_view),
    path('logout/', email_views.logout_btn_view),
    # ---- #
    path("verify/<uuid:token>/", email_views.verify_email_token_view),
    path("courses/", include("courses.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    # Way of adding new element in an array.
    # directory for user-uploaded content. Django will automatically
    # recognize this directory and put any files uploaded to the server.
    # For development only.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    pass
