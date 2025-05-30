from clients.sendgrid_client import send_email

class InvitationManager:

    # need to pass request
    def send_invitation(self, email: str, link: str) -> bool:
        return send_email()