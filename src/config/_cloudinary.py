# the '_' of this filename is needed so that this file can be distinguished from the
# thrid party cloudinary file

import cloudinary
# This lets us access key-value pairs in .env
from decouple import config

#first parameter is the key name in .env
CLOUDINARY_CLOUD_NAME = config("CLOUDINARY_CLOUD_NAME", default="")
CLOUDINARY_PUBLIC_KEY = config("CLOUDINARY_PUBLIC_KEY", default="")
CLOUDINARY_SECRET_KEY = config("CLOUDINARY_SECRET_KEY", default="")

def cloudinary_init():
    # Configuration       
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUD_NAME, 
        api_key = CLOUDINARY_PUBLIC_KEY, 
        api_secret = CLOUDINARY_SECRET_KEY, # Click 'View API Keys' above to copy your API secret
        secure=True
    )

    print("Cloudinary is initialized!")