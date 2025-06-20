from abc import ABC, abstractmethod
from clients.supabase_client import supabase_admin
# we we
class UserFactory(ABC): 
    def __init__(self):
        self.supabase = supabase_admin

    @abstractmethod
    def create_user(self, user_id):
        pass

    def _record_exists(self, table, column, user_id):
        response = self.supabase.table(table).select(column).eq(column, user_id).execute()
        print(f"Checking record in {table}.{column} for user {user_id}: {response.data}")
        return bool(response.data)

class CreateCitizen(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("users").update({"role": "citizen"}).eq("id", user_id).execute()
        
        if not self._record_exists("citizens", "citizen_id", user_id):
            self.supabase.table("citizens").insert({
                "citizen_id": user_id
            }).execute()

        return 1
    
class CreateAdmin(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("users").update({"role": "administrator"}).eq("id", user_id).execute()
        if not self._record_exists("admins", "admin_id", user_id):
            self.supabase.table("admins").insert({
                "admin_id": user_id
            }).execute()

        return user_id
    
class CreateMaintenanceCompany(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("users").update({"role": "maintenance_company"}).eq("id", user_id).execute()
        if not self._record_exists("maintenance_companies", "maintenance_company_id", user_id):
            self.supabase.table("maintenance_companies").insert({
                "maintenance_company_id": user_id
            }).execute()

        return user_id
    
class CreateGovtBody(UserFactory):
    def create_user(self, user_id):
        self.supabase.table("users").update({"role": "govt_body"}).eq("id", user_id).execute()
        if not self._record_exists("government_bodies", "goverment_body_id", user_id):
            self.supabase.table("government_bodies").insert({
                "goverment_body_id": user_id
            }).execute()

        return user_id