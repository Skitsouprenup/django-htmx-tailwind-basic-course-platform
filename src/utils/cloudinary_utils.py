import uuid
from django.template.loader import get_template
from django.utils import text

import config

def generate_public_id(model):

    title = model.title
    unique_id = str(uuid.uuid4()).replace("-", "")
    if not title:
        return unique_id
    slug = text.slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"
        

def get_public_id_prefix(model):
    public_id = model.public_id
    if public_id:
        return f"courses/{public_id}"
    return f"courses"

def get_thumbnail(image, as_html=False, width=300):
    if not image:
        return ""
    options = {
        "width": width,
    }

    if(as_html):
        return image.image(**options)

    url = image.build_url(**options)
    return url

def get_video(
    model, 
    as_html=False, 
    width=None,
    height=None,
    #determines if video is private or not
    #false if public
    sign_url=False,
    fetch_format="auto",
    quality="auto",
    controls=True,
    autoplay=True
):
    if not hasattr(model, 'video'):
        return ""
    options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay
    }

    if width is not None:
        options['width'] = width
    if height is not None:
        options['height'] = height
    if height and width:
        options['crop'] = "limit"

    url = model.video.build_url(**options)

    if(as_html):
        template_name = "snippets/videos/embed.html"
        template = get_template(template_name)
        cld_name = config.CLOUDINARY_CLOUD_NAME
        _html = template.render({
            "video_url":url, 
            "cloud_name":cld_name,
            "base_color":"#007cae"
        })
        return _html

    return url