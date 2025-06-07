from interfaces.complaint_builder_interface import CaseComponentBuilder
class ComplaintBuilder(CaseComponentBuilder):
    def __init__(self):
        self.complaint = {}

    def setCitizenID(self, citizen_id):
        self.complaint['citizen_id'] = citizen_id
    
    def setHeader(self, header):
        self.complaint['complaint_title'] = header

    def setDetails(self, details):
        self.complaint['complaint_description'] = details        

    # def setFollowUp(self, followUp):
    #     self.complaint['followUp'] = followUp

    # def setUpdatedAt(self, updated_at):
    #     self.complaint['updated_at'] = updated_at
