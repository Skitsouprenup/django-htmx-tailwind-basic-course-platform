from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    #<data-type/field:parameter-name>
    #'slug' is a 'path converter'.
    # source for 'path converter': https://docs.djangoproject.com/en/5.2/topics/http/urls/#path-converters
    path('<slug:course_id>/', views.course_detail_view),
    path('<slug:course_id>/lesson/<slug:lesson_id>/', views.lesson_detail_view),
    path('', views.course_list_view)
]