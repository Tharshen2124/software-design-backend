from datetime import datetime, timedelta
from clients.sendgrid_client import send_email
from clients.supabase_client import supabase
from django.utils import timezone
import pytz  

class InvitationManager:

    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_invitation(self, invitation_id:str) -> dict:
        try:
            response = supabase.table('invitations')\
                .select('*')\
                .eq('invitation_id', invitation_id)\
                .execute()
            return response.data[0] if response.data else None
        
        except Exception as e:
            print(f"Error getting invitation: {str(e)}")
            return None

    
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

    def mark_invitation_as_used(self, invitation_id: str, user_id: str) -> bool:
        try:
            # get the invitation
            invitation = supabase.table('invitations')\
                .select('*')\
                .eq('invitation_id', invitation_id)\
                .execute().data
            
            if not invitation:
                print("No valid invitation found")
                return False
            
            invitation = invitation[0]
            role = invitation.get('role')

            if not role:
                print("No role found in invitation")
                return False
            
            # update user role
            user_update = supabase.table('users')\
                .update({'role': role})\
                .eq('id', user_id)\
                .execute()
            
            print(f"User update response: {user_update}")
            
            # update invitation
            invitation_update = supabase.table('invitations')\
                .update({
                    'isexpired': True,
                    'user_id': user_id,
                    'updated_at': datetime.now(timezone.utc).isoformat()
                })\
                .eq('invitation_id', invitation_id)\
                .execute()
            
            print(f"Invitation update response: {invitation_update}")
            
            return True
            
        except Exception as e:
            print(f"Error in mark_invitation_as_used: {str(e)}")
            # Attempt to revert user role if possible
            try:
                supabase.table('users')\
                    .update({'role': 'citizen'})\
                    .eq('id', user_id)\
                    .execute()
            except:
                pass
            return False
    
    def validate_invitation(self, invitation_id:str) -> bool:
        try:
            invitation = self.get_invitation(invitation_id)

            if not invitation:
                return False
            
            # Check if already used
            if invitation.get('isexpired') or invitation.get('user_id'):
                return False
            
            # Check expiration (1 day limit)
            created_at_str = invitation.get('created_at')
            if not created_at_str:
                return False

            # Convert string to datetime object
            created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))

            # If the datetime is already timezone-aware, use it directly
            if created_at.tzinfo is not None:
                expiration_time = created_at + timedelta(days=1)
                return timezone.now() < expiration_time
            else:
                # If naive, make it aware (though Supabase usually returns aware datetimes)
                created_at = timezone.make_aware(created_at)
                expiration_time = created_at + timedelta(days=1)
                return timezone.now() < expiration_time
        
        except Exception as e:
            print(f"Error validating invitation: {str(e)}")
            return False