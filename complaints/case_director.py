from interfaces.complaint_builder_interface import CaseComponentBuilder
from .adapters.complaint_adapter import ComplaintData
from .adapters.maintenance_adapter import MaintenanceProjectData

# builds the complaint based on the interface using the data provided 
class CaseDirector:
   def buildComplaints(self, builder: CaseComponentBuilder, data: ComplaintData):
      builder.setHeader(data.title)
      builder.setDetails(data.description)
      builder.setCitizenID(data.citizen_id)
      builder.setStatus(data.status)
      builder.setImage(data.image_url)

      return builder.complaint
   
   def buildMaintenanceProject(self, builder: CaseComponentBuilder, data: MaintenanceProjectData):
      builder.setHeader(data.title)
      builder.setDetails(data.description)
      builder.setStatus(data.status)
      builder.setComplaintIds(data.complaint_ids)
      builder.setMaintenanceCompanyId(data.maintenance_company_id)
      print(data.complaint_ids)
      return builder.maintenance_plan