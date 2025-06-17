from abc import ABC, abstractmethod
from clients.supabase_client import supabase_admin

class UserFactory(ABC): 
    def __init__(self):
        self.supabase = supabase_admin

    @abstractmethod
    def create_user(self, user_id):
        pass

class CreateCitizen(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("citizens").insert({
            "citizen_id": user_id
        }).execute()

        return 1
    
class CreateAdmin(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("admins").insert({
            "admin_id": user_id
        }).execute()

        return user_id
    
class CreateMaintenanceCompany(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("maintenance_companies").insert({
            "maintenance_company_id": user_id
        }).execute()

        return user_id
    
class CreateGovtBody(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("government_bodies").insert({
            "government_body_id": user_id
        }).execute()

        return user_id