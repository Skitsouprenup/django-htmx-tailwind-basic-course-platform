#render(HttpRequest, template_name, context)
from django.shortcuts import render
from django.http import Http404

from courses import services

from utils import cloudinary_utils as cl_utils

# Create your views here.
# Note: template paths here are relative to the path in 
# 'DIRS' in 'TEMPLATES' in 'settings.py'

def course_list_view(request):
    queryset = services.get_published_courses()
    context = {
        "published_courses": queryset
    }
    return render(request, "courses/list.html", context)

def course_detail_view(request, course_id=None):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404

    # get all lessons that's related to this course via
    # foreign key or other types of relationship
    lessons_queryset = services.get_course_lessons(course_obj)
    context = {
        "course": course_obj,
        "lessons": lessons_queryset
    }
    return render(request, "courses/detail.html", context)

def lesson_detail_view(request, course_id=None, lesson_id=None):
    lesson = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson is None:
        raise Http404
    
    context = {
        "lesson": lesson
    }

    email_id = request.session.get('email_id')
    if lesson.requires_email and not email_id:
        request.session['next_url'] = request.path
        return render(request, "courses/email-required.html", {})

    template_name = "courses/lesson-soon.html"
    if not lesson.is_coming_soon and lesson.has_video:
        template_name = "courses/lesson.html"
        context['video_embed'] = cl_utils.get_video(lesson, True, 640, 480)

    return render(request, template_name, context)
