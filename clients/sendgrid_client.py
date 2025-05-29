import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_simple_message():
	message = Mail(
		from_email='hehe@gmail.com',
		to_emails='wee@gmail.com',
		subject='Sending with Twilio SendGrid is Fun',
		html_content='<strong>with response</strong>')
	try:
		sg = SendGridAPIClient(os.environ.get('SENDGRID_KEY'))
		response = sg.send(message)
		print(response.status_code)
		print(response.body)
		print(response.headers)
		return response
	except Exception as e:
		print(str(e))