from django.db import models
from courses.choices import AccessRequirement, PublishStatus
from cloudinary import CloudinaryField

# Create your models here.

class Course(models.Model):
    def img_upload(instance, filename):
        return f"{filename}"

    title = models.CharField(max_length=120)
    # 'blank=True' means this field in a view, can have
    # empty value. 'null=True' means that this field in database,
    # can have null values.
    description = models.TextField(blank=True, null=True)
    access = models.CharField(
        max_length=25,
        choices=AccessRequirement.choices,
        default=AccessRequirement.ANYONE
    )
    status = models.CharField(
        max_length=25,
        choices=PublishStatus.choices,
        default=PublishStatus.DRAFT
    )
    # Use this to upload images directly to your server.
    # Development only.
    #image = models.ImageField(upload_to=img_upload)
    #Use this to upload images to cloudinary.
    image = models.CloudinaryField("image", null=True)
