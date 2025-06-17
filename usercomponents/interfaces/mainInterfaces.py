from abc import ABC, abstractmethod
from .dashboardInterfaces import (
    AdminDashboard,
    CitizenDashboard,
    MaintenanceCompanyDashboard,
    GovtBodyDashboard,
    Dashboard
)
from .analyticInterfaces import (
    AdminAnalytics,
    CitizenAnalytics,
    MaintenanceCompanyAnalytics,
    GovtBodyAnalytics,
    Analytics
)

# interface class
class UserComponentFactory(ABC):
    @abstractmethod
    def createDashboard(self) -> Dashboard:
        pass

    @abstractmethod
    def createAnalytics(self) -> Analytics:
        pass

## concrete classes
class CitizenComponent(UserComponentFactory):
    def __init__(self, request):
        self.request = request

    def createDashboard(self) -> Dashboard:
        return CitizenDashboard()
    
    def createAnalytics(self) -> Analytics:
        user_id = self.request.GET.get("user_id")
        timeline = self.request.GET.get("timeline", "30days").lower()
        year = self.request.GET.get("year")

        return CitizenAnalytics(user_id, timeline, year)
    
class AdminComponent(UserComponentFactory):
    def __init__(self, request):
        self.request = request

    def createDashboard(self) -> Dashboard:
        return AdminDashboard()
    
    def createAnalytics(self) -> Analytics:
        timeline = self.request.GET.get("timeline", "30days").lower()
        year = self.request.GET.get("year")
        return AdminAnalytics(timeline, year)
    
class MaintenanceCompanyComponent(UserComponentFactory):
    def __init__(self, request):
        self.request = request

    def createDashboard(self) -> Dashboard:
        return MaintenanceCompanyDashboard()
    
    def createAnalytics(self) -> Analytics:
        timeline = self.request.GET.get("timeline", "30days").lower()
        year = self.request.GET.get("year")
        return MaintenanceCompanyAnalytics(timeline, year)
    
class GovtBodyComponent(UserComponentFactory):
    def __init__(self, request):
        self.request = request

    def createDashboard(self) -> Dashboard:
        return GovtBodyDashboard()
    
    def createAnalytics(self) -> Analytics:
        timeline = self.request.GET.get("timeline", "30days").lower()
        year = self.request.GET.get("year")
        return GovtBodyAnalytics(timeline, year)