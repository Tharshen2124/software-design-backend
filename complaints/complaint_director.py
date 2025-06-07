from interfaces.complaint_builder_interface import CaseComponentBuilder
from .complaint_adapter import ComplaintData

# builds the complaint based on the interface using the data provided 
class ComplaintDirector:
   def buildComplaints(self, builder: CaseComponentBuilder, data: ComplaintData):
        builder.setHeader(data.title)
        builder.setDetails(data.description)
        builder.setCitizenID(data.citizen_id)
        builder.setStatus(data.status)

        return builder.complaint