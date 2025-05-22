from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    #<data-type/field:parameter-name>
    #'slug' here is a member of a model which is a string.
    #Thus, the data-type of course_id is string
    path('<slug:course_id>/', views.course_detail_view),
    path('<slug:course_id>/lesson/<slug:lesson_id>/', views.lesson_detail_view),
    path('', views.course_list_view),
]