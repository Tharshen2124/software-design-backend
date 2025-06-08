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
        return "Citizen dashboard setup complete"

class MaintenanceCompanyDashboard(Dashboard):
    def setupDashboard(self):
        return "Maintenance company dashboard setup complete"

class GovtBodyDashboard(Dashboard):
    def setupDashboard(self):
        return "Government body dashboard setup complete"
