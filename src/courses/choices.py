from django.db import models

class AccessRequirement(models.TextChoices):
        #'any' is the value that's going to database
        #'Anyone' is the label in the views
        #this syntax is called 'tuple packing'
        ANYONE = 'any', 'Anyone'
        EMAIL_REQUIRED = 'email_required', 'Email Required'

class PublishStatus(models.TextChoices):
    PUBLISHED = 'published', 'Published'
    SOON = 'soon', 'Soon'
    DRAFT = 'draft', 'Draft'