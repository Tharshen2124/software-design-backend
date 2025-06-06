from .status_enum import Status

# DTO for Complaint data
class ComplaintData:
    def __init__(self, title, description, citizen_id, status):
        self.title = title
        self.description = description
        self.citizen_id = citizen_id
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

            if not title or not description or not citizen_id:
                raise ValueError("Missing required fields")

            try:
                status_enum = Status(status_str)
            except ValueError:
                raise ValueError(f"Invalid status value: {status_str}")

            return ComplaintData(title, description, citizen_id, status_enum)

        except Exception as e:
            raise ValueError(str(e))
