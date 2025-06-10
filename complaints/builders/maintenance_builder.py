from interfaces.complaint_builder_interface import CaseComponentBuilder

class MaintenanceProjectBuilder(CaseComponentBuilder):
    def __init__(self):
        self.maintenance_plan = {}

    def setHeader(self, header):
        self.maintenance_plan['project_title'] = header

    def setDetails(self, details):
        self.maintenance_plan['project_description'] = details        

    def setImage(self, image):
        self.maintenance_plan['project_image_url'] = image

    def setStatus(self, status):
        self.maintenance_plan['status'] = status.value

    # def setFollowUp(self, followUp):
    #     self.maintenance_plan['followUp'] = followUp

    # def setUpdatedAt(self, updated_at):
    #     self.maintenance_plan['updated_at'] = updated_at
