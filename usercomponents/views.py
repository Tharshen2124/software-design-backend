from django.http import JsonResponse
from django.shortcuts import redirect
from usercomponents.interfaces.mainInterfaces import (
    AdminComponent,
    CitizenComponent,
    MaintenanceCompanyComponent,
    GovtBodyComponent
)

# Map roles to their corresponding factories
ROLE_FACTORY_MAP = {
    "administrator": AdminComponent,
    "citizen": CitizenComponent,
    "maintenance_company": MaintenanceCompanyComponent,
    "govt_body": GovtBodyComponent,
}

class UserComponentAdapter: 
    def display_dashboard(request):
        # user = request.user
        role = 'administrator'

        factory_class = ROLE_FACTORY_MAP.get(role)

        if factory_class is None:
            raise ValueError(f"Unknown role: {role}")
        
        factory = factory_class()
        dashboard_data = factory.createDashboard()
        analytics_data = factory.createAnalytics()

        data = {
            "message": "Dashboard rendered successfully.",
            "dashboard": dashboard_data.setupDashboard(),
            "analytics": analytics_data.setupAnalytics()
        }
        
        return JsonResponse (data)

