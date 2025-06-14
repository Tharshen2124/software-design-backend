from ..status_enum import Status
from clients.cloudinary_client import CloudinaryClient

# DTO for Complaint data
class ComplaintData:
    def __init__(self, title, description, citizen_id, image_url, status):
        self.title = title
        self.description = description
        self.citizen_id = citizen_id
        self.image_url = image_url
        self.status = status

# Decouple raw HTTP request values to Python-code structure
class ComplaintAdapter:
    @staticmethod
    def get_data(request):
        try:            
            title = request.POST.get("complaint_title")
            description = request.POST.get("complaint_description")
            citizen_id = request.POST.get("citizen_id")
            status_str = request.POST.get("status", "pending")
            image = request.FILES.get("complaint_image")

            if not title or not description or not citizen_id or not image:
                raise ValueError("Missing required fields")

            try:
                status_enum = Status(status_str)
            except ValueError:
                raise ValueError(f"Invalid status value: {status_str}")
            
            cloudinary_client = CloudinaryClient()
            image_url = (cloudinary_client.upload(image)).get('secure_url')

            return ComplaintData(title, description, citizen_id, image_url, status_enum)

        except Exception as e:
            raise ValueError(str(e))
