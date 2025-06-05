from abc import ABC, abstractmethod

class ComplaintComponentBuilder(ABC):
    @abstractmethod
    def setHeader(self, header):
        pass

    @abstractmethod
    def setDetails(self, details):
        pass

    # @abstractmethod
    # def setFollowUp(self, followUp):
    #     pass

    @abstractmethod
    def setStatus(self, status):
        pass

    # @abstractmethod
    # def setUpdatedAt(self, updated_at):
    #     pass
