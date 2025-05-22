#render(HttpRequest, template_name, context)
from django.shortcuts import render
from django.http import Http404, JsonResponse

from courses import services

# Create your views here.

def course_list_view(request):
    queryset = services.get_published_courses()
    return JsonResponse({ "data": [x.path for x in queryset] })
    return render(request, "courses/list.html", {})

def course_detail_view(request, course_id=None):
    course_obj = services.get_course_detail(course_id=course_id)
    if course_obj is None:
        raise Http404
    
    # get all lessons that's related to this course via
    # foreign key or other types of relationship
    lessons_queryset = course_obj.lesson_set.all()
    return JsonResponse({
        "data": course_obj.id, 
        "lessons_id":[x.path for x in lessons_queryset]
    })
    return render(request, "courses/detail.html", {})

def lesson_detail_view(request, course_id=None, lesson_id=None):
    lesson_obj = services.get_lesson_detail(course_id=course_id, lesson_id=lesson_id)
    if lesson_obj is None:
        raise Http404
    
    return JsonResponse({"data": lesson_obj.id})
    return render(request, "courses/lesson.html", {})
