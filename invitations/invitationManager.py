from clients.sendgrid_client import send_email

class InvitationManager:

    def send_invitation(self, email: str, link: str) -> bool:
        return send_email(email,link)