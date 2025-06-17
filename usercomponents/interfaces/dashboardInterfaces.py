from abc import ABC, abstractmethod

# Interface
class Dashboard(ABC):
    @abstractmethod
    def setupDashboard(self):
        pass

# Concrete classes
class AdminDashboard(Dashboard):
    def setupDashboard(self):
        title = "Analytics Dashboard."
        description = "Track complaint trends and monitor resolution status across the platform."
        return {
            "title": title,
            "description": description
        }

class CitizenDashboard(Dashboard):
    def setupDashboard(self):
        title = "My Complaints Overview."
        description = "Track your submitted complaints and the overall status."
        return {
            "title": title,
            "description": description
        }

class MaintenanceCompanyDashboard(Dashboard):
    def setupDashboard(self):
        title = "Task Overview."
        description = "Track assigned tasks and their resolution status."
        return {
            "title": title,
            "description": description
        }

class GovtBodyDashboard(Dashboard):
    def setupDashboard(self):
        title = "Maintenance Projects Overview."
        description = "Track filtered complaints, approved projects, and their resolution status."
        return {
            "title": title,
            "description": description
        }
