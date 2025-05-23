from courses.models import Course, Lesson , PublishStatus, AccessRequirement

def get_courses():
    return Course.objects.all()

def get_published_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

def get_course_detail(course_id=None):
    if course_id is None:
        return None
    
    obj = None
    try:
        obj = Course.objects.get(
            status=PublishStatus.PUBLISHED,
            public_id=course_id
        )
    except:
        pass
    return obj

def get_course_lessons(instance):
    # Lesson.objects.none() returns an empty queryset(list) of
    # 'Lesson' model
    lessons = Lesson.objects.none()
    if isinstance(instance, Course):
        lessons = instance.lesson_set.filter(
            course_foreign__status=PublishStatus.PUBLISHED,
            status=PublishStatus.PUBLISHED,
        )
    return lessons

def get_lesson_detail(course_id=None, lesson_id=None):
    if lesson_id is None or course_id is None:
        return None
    
    obj = None
    try:
        # use __ to access columns of a
        # foreign table
        obj = Lesson.objects.get(
            course_foreign__public_id=course_id,
            course_foreign__status=PublishStatus.PUBLISHED,
            status=PublishStatus.PUBLISHED,
            public_id=lesson_id
        )
    except Exception as e:
        print("get_lesson_detail", e)
    return obj