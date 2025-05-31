import uuid
from clients.sendgrid_client import send_email
from clients.supabase_client import supabase

class InvitationManager:
    
    def create_invitation(self, email:str, role:str) -> bool:
        data = {
            'role': role,
            'email':email,
        }

        try:
            res = supabase.table('invitations').insert(data).execute()
            return res.status_code == 201
        except Exception as e:
            return False

    def send_invitation(self, email: str, link: str) -> bool:
        return send_email(email,link)