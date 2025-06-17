from abc import ABC, abstractmethod
from clients.supabase_client import supabase_admin

class UserFactory(ABC): 
    def __init__(self):
        self.supabase = supabase_admin

    @abstractmethod
    def create_user(self, user_id):
        pass

    def _record_exists(self, table, column, user_id):
        response = self.supabase.table(table).select(column).eq(column, user_id).maybe_single().execute()
        return response.data is not None

class CreateCitizen(UserFactory):
    def create_user(self, user_id):
        if not self._record_exists("citizens", "citizen_id", user_id):
            self.supabase.table("citizens").insert({
                "citizen_id": user_id
            }).execute()

        return 1
    
class CreateAdmin(UserFactory):
    def create_user(self, user_id):
        if not self._record_exists("admins", "admin_id", user_id):
            self.supabase.table("admins").insert({
                "admin_id": user_id
            }).execute()

        return user_id
    
class CreateMaintenanceCompany(UserFactory):
    def create_user(self, user_id):
        if not self._record_exists("maintenance_companies", "maintenance_company_id", user_id):
            self.supabase.table("maintenance_companies").insert({
                "maintenance_company_id": user_id
            }).execute()

        return user_id
    
class CreateGovtBody(UserFactory):
    def create_user(self, user_id):
        if not self._record_exists("government_bodies", "government_body_id", user_id):
            self.supabase.table("government_bodies").insert({
                "government_body_id": user_id
            }).execute()

        return user_id