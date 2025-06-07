from abc import ABC, abstractmethod

class CaseComponentBuilder(ABC):
    @abstractmethod
    def setHeader(self, header):
        pass

    @abstractmethod
    def setDetails(self, details):
        pass

    # @abstractmethod
    # def setFollowUp(self, followUp):
    #     pass

    def setStatus(self, status):
        self.complaint['status'] = status.value

    # @abstractmethod
    # def setUpdatedAt(self, updated_at):
    #     pass
