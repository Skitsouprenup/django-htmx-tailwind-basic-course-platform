from cloudinary import CloudinaryImage
from django.contrib import admin
from .models import Course, Lesson
from django.utils.html import format_html

from utils import cloudinary_utils as cl_utils

# This class adds options for the model in this class
# to the other model that is assigned to the other model's
# inline list in the django admin panel. 
class LessonInline(admin.StackedInline):
    model=Lesson
    #Fields in this list can't be modified in the panel
    readonly_fields=[
        'public_id',
        'updated',
        'created_at',
        'image_view',
        'video_view'
    ]
    # This removes extra form entries of lessons in the admin panel
    extra = 0

    # This function represents the image_view field.
    # 'obj' is the model where this function is assigned.
    # In this case, Lesson model.
    # This is not gonna be a column in the database.
    def image_view(self, obj):
        url = cl_utils.get_thumbnail(obj.thumbnail, False)
        return format_html(f"<img src={url} />")
    image_view.short_description = 'Current Image'

    def video_view(self, obj):
        video_template = cl_utils.get_video(obj, True, 300, 300)
        return video_template
    image_view.short_description = 'Current Video'

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines=[LessonInline]
    #Fields in the model that is displayed in model table list
    list_display = ['title', 'status', 'access']
    # Filter options. This will create additional interface
    # on the right side of the panel.
    list_filter = ['status', 'access']
    # Fields in the model that django admin can access.
    # image_view is a custom member that is not a member
    # of the model
    fields = ['title','public_id','description', 'status', 'image', 
              'access', 'image_view']
    #Fields in this list can't be modified in the panel
    readonly_fields=['public_id','image_view']

    # This function represents the image_view field.
    # 'obj' is the model where this function is assigned
    # This is not gonna be a column in the database.
    def image_view(self, obj):
        #url = obj.image.url
        cloudinary_id = str(obj.image)
        #print(url)

        # Alternative way to transform images in cloudinary.
        # Make sure the field type of the 'image' field is
        # CloudinaryField.
        # img = obj.image.image(width=300)

        #CloudinaryImage returns html syntax
        html_img = CloudinaryImage(cloudinary_id).image(width=300)

        # format_html sanitizes and parses html syntax
        # to be displayed in the panel
        return format_html(html_img)

    # Function attribute. This changes that description
    # of the field in the panel
    image_view.short_description = 'Current Image'

# Register your models here.
#admin.site.register(Course)