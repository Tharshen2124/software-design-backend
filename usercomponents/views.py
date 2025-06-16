from django.http import JsonResponse
from django.shortcuts import redirect
from clients.supabase_client import supabase
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
        user_id = request.GET.get('user_id')
        

        if not user_id:
            return JsonResponse({'error': 'user_id is required'}, status=400)
        
        try: 
            response = supabase.table('users').select('role').eq('id', user_id).execute()

            role = response.data[0]['role']

        except Exception as e:
            print("Supabase fetch error:", e)
            return JsonResponse({"error": "Failed to fetch role from Supabase"}, status=500)

        factory_class = ROLE_FACTORY_MAP.get(role)

        if factory_class is None:
            raise ValueError(f"Unknown role: {role}")
        
        factory = factory_class(request)
        dashboard_data = factory.createDashboard()
        analytics_data = factory.createAnalytics()

        data = {
            "role": role,
            "message": "Dashboard rendered successfully.",
            "dashboard": dashboard_data.setupDashboard(),
            "analytics": analytics_data.setupAnalytics()
        }
        
        return JsonResponse (data)