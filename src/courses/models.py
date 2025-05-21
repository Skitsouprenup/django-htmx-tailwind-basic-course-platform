from django.utils import timezone
from django.db import models
from courses.choices import AccessRequirement, PublishStatus
from cloudinary.models import CloudinaryField

from utils import cloudinary_utils as cl_utils

# Create your models here.

class Course(models.Model):

    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=150, default="", null=True)
    # 'blank=True' means this field in a view, can have
    # empty value. 'null=True' means that this field in database,
    # can have null values.
    description = models.TextField(blank=True, null=True)
    access = models.CharField(
        max_length=25,
        choices=AccessRequirement.choices,
        default=AccessRequirement.EMAIL_REQUIRED
    )
    status = models.CharField(
        max_length=25,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
    )

    # Use this to upload images directly to your server.
    # Development only.
    # def img_upload(instance, filename):
    #    return f"{filename}"
    #image = models.ImageField(upload_to=img_upload)

    @property
    def get_display_name(self):
        if self.title:
            return self.title
        
        # __class__ returns a reference for the current model
        # __name__ returns the class name
        model_name = self.__class__.__name__
        return f"${model_name} Course"

    #Use this to upload images to cloudinary.
    image = CloudinaryField(
        "image", 
        null=True, 
        public_id_prefix=cl_utils.get_public_id_prefix,
        display_name=get_display_name,
        tags= ['course', 'thumbnail', 'image']
    )

    # auto_now_add only happens one time; once a new column is
    # is created. If you already have record in your database use
    # the 'default' parameter.
    created_at = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    # This function is called by django when we insert 
    # a record to our database. We can override it and insert
    # some tasks before calling the original save() function.
    # *args and **kwargs parameters are optional
    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = cl_utils.generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def path(self):
        return f"/courses/{self.public_id}"

    @property
    def get_absolute_url(self):
        return self.path

    @property
    def is_published(self):
        return self.status() == PublishStatus.PUBLISHED
    

class Lesson(models.Model):

    @property
    def get_display_name(self):
        return f"{self.title} = {self.course_foreign.get_display_name()}"

    #This variable will generate the 'course_id' column in the
    #database. Thus, you can't use the name to declare a new
    #field in this class.
    course_foreign = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    public_id = models.CharField(max_length=150, default="", null=True)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField(
        'image', 
        blank=True, 
        null=True,
        public_id_prefix=cl_utils.get_public_id_prefix,
        display_name=get_display_name,
        tags=['lesson', 'thumbnail', 'image']
    )
    video = CloudinaryField(
        'video', 
        blank=True, 
        null=True, 
        resource_type='video',
        public_id_prefix=cl_utils.get_public_id_prefix,
        display_name=get_display_name,
        tags=['lesson', 'video'],
        type="private"
    )
    preview = models.BooleanField(
        default=False, 
        help_text="True if can be viewed by anyone. Otherwise, false."
    )
    status = models.CharField(
        max_length=25,
        choices=PublishStatus.choices,
        default=PublishStatus.PUBLISHED
    )

    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.public_id == "" or self.public_id is None:
            self.public_id = cl_utils.generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def path(self):
        course_path = self.course_foreign.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"

    # Special class that is recognized by django.
    class Meta:
        # '-' before the name means 'reverse' order.
        # '-updated' is a second sort option if two
        # or more orders are identical.
        ordering = ['order', '-updated']
    

