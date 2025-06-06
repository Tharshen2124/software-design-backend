from interfaces.complaint_builder_interface import ComplaintComponentBuilder
from status_enum import Status

class ComplaintDirector:
    def buildComplaints(self, builder: ComplaintComponentBuilder, request):
        builder.setHeader(request.POST.get("complaint_title"))
        builder.setDetails(request.POST.get("complaint_description"))
        builder.setCitizenID(request.POST.get("citizen_id"))
        try:
            status_enum = Status(request.POST.get("status", "pending"))
        except ValueError:
            raise ValueError(f"Invalid status value.")
        
        builder.setStatus(status_enum)

        return builder.complaint