from ..status_enum import Status
from clients.cloudinary_client import CloudinaryClient

# DTO for Maintenance Project data
class MaintenanceProjectData:
    def __init__(self, title, description, status, complaint_ids, maintenance_company_id, image_url, maintenance_project_id, follow_up):
        self.title = title
        self.description = description
        self.status = status
        self.complaint_ids = complaint_ids
        self.maintenance_company_id = maintenance_company_id
        self.image_url = image_url
        self.maintenance_project_id = maintenance_project_id  
        self.follow_up = follow_up  

class MaintenanceProjectAdapter:
    @staticmethod
    def get_data(request):
        try:
            title = request.POST.get("project_title")
            description = request.POST.get("project_description")
            status_str = request.POST.get("status", "pending")
            maintenance_company_id = request.POST.get("maintenance_company_id")
            raw_ids = request.POST.get('complaint_ids')
            print(raw_ids)
            
            if not title or not description or not maintenance_company_id or not raw_ids:
                raise ValueError("Missing required fields")
            
            complaint_ids = [int(id.strip()) for id in raw_ids.split(',') if id.strip().isdigit()]
            
            try:
                status_enum = Status(status_str)
            except ValueError:
                raise ValueError(f"Invalid status value: {status_str}")

            return MaintenanceProjectData(title, description, status_enum, complaint_ids, maintenance_company_id, None, None)

        except Exception as e:
            raise ValueError(str(e))
    
    def get_data_for_update(request):
        try:
            status_str = request.POST.get("status")
            maintenance_project_id = request.POST.get("maintenance_project_id")
            follow_up = request.POST.get("follow_up")

            print("Adapter Data for Update:")
            print(f"Status: {status_str}, Maintenance Project ID: {maintenance_project_id}, Follow Up: {follow_up}")

            if not status_str or not maintenance_project_id:
                raise ValueError("Missing required fields")

            try:
                status_enum = Status(status_str)
            except ValueError:
                raise ValueError(f"Invalid status value: {status_str}")

            project_image = request.FILES.get("project_image")

            if not project_image:
                return MaintenanceProjectData(None, None, status_enum, None, None, None, maintenance_project_id, None)
            else:
                project_image = request.FILES.get("project_image")
                cloudinary_client = CloudinaryClient()
                image_url = (cloudinary_client.upload(project_image)).get('secure_url')
                return MaintenanceProjectData(None, None, status_enum, None, None, image_url, maintenance_project_id, follow_up)

        except Exception as e:
            raise ValueError(str(e))
    