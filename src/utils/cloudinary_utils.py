import uuid
from django.utils import text

def generate_public_id(model):
    title = model.title
    slug = text.slugify(title)
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    return f"{slug}-{unique_id[:5]}"
        

def get_public_id_prefix(model):
    title = model.title
    if title:
        slug = text.slugify(title)
        unique_id = str(uuid.uuid4()).replace("-", "")[:5]
        return f"courses/{slug}-{unique_id}"
    return "courses"

def get_display_name(model):
    title = model.title
    if title:
        return title
    return 'Course Image'