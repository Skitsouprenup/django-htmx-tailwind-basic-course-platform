from courses.models import Course, PublishStatus, AccessRequirement

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

def get_lesson_detail(course_id = None, lesson_id=None):
    if lesson_id is None or course_id is None:
        return None
    
    obj = None
    try:
        # use __ to access columns of a
        # foreign table
        obj = Course.objects.get(
            course__id=course_id,
            course__status=PublishStatus.PUBLISHED,
            status=PublishStatus.PUBLISHED,
            id=lesson_id
        )
    except Exception as e:
        print("get_lesson_detail", e)
    return obj