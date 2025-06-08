# Analytics interfaces
from abc import ABC, abstractmethod

# interface class
class Analytics(ABC):
    @abstractmethod
    def setupAnalytics(self):
        pass

# concrete classes
class AdminAnalytics(Analytics):
    def setupAnalytics(self):
        return super().setupAnalytics()
    
class CitizenAnalytics(Analytics):
    def setupAnalytics(self):
        return super().setupAnalytics()
    
class MaintenanceCompanyAnalytics(Analytics):
    def setupAnalytics(self):
        return super().setupAnalytics()
    
class GovtBodyAnalytics(Analytics):
    def setupAnalytics(self):
        return super().setupAnalytics()