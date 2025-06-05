from interfaces.complaint_builder_interface import ComplaintComponentBuilder

class ComplaintDirector:
    def buildComplaints(self, builder: ComplaintComponentBuilder, request):
        builder.setHeader(request.POST.get("complaint_title"))
        builder.setDetails(request.POST.get("complaint_description"))
        builder.setCitizenID(request.POST.get("citizen_id"))
        builder.setStatus(request.POST.get("status"))

        return builder.complaint