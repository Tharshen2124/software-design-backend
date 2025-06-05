import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv

load_dotenv()

# This class is a singleton that manages the Cloudinary client configuration
class CloudinaryClient:
    _instance = None  

    # ensures a single instance of CloudinaryClient is created and reused
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cloudinary.config(
                cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
                api_key=os.getenv("CLOUDINARY_API_KEY"),
                api_secret=os.getenv("CLOUDINARY_API_SECRET"),
                secure=True,
            )
        return cls._instance

    def upload(self, file_path_or_url, public_id=None, **options):
        return cloudinary.uploader.upload(file_path_or_url, public_id=public_id, **options)

    def url(self, public_id, **transformation_options):
        url, _ = cloudinary_url(public_id, **transformation_options)
        return url
