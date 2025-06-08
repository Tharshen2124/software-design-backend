from ..status_enum import Status
from clients.cloudinary_client import CloudinaryClient

# DTO for Maintenance Project data
class MaintenanceProjectData:
    def __init__(self, title, description, image_url, status):
        self.title = title
        self.description = description
        self.image_url = image_url
        self.status = status

class MaintenanceProjectAdapter:
    @staticmethod
    def get_data(request):
        try:
            title = request.POST.get("project_title")
            description = request.POST.get("project_description")
            status_str = request.POST.get("status", "pending")
            image = request.FILES.get("project_image")
            print(request.FILES.get("complaint_image"))

            if not title or not description or not image:
                raise ValueError("Missing required fields")

            try:
                status_enum = Status(status_str)
            except ValueError:
                raise ValueError(f"Invalid status value: {status_str}")

            cloudinary_client = CloudinaryClient()
            image_url = (cloudinary_client.upload(image)).get('secure_url')

            return MaintenanceProjectData(title, description, image_url, status_enum)

        except Exception as e:
            raise ValueError(str(e))