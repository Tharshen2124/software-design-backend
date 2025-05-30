import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(email, link):
	message = Mail(
		from_email= os.environ.get('SENDER_EMAIL'),
		to_emails=email,
		subject='Sending with Twilio SendGrid is Fun',
		html_content=f'<strong>{link}</strong>')
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
		response = sg.send(message)
		return response
	except Exception as e:
		print(str(e))