# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from clients.sendgrid_client import send_simple_message  # Adjust import path

def test_email(request):
    response = send_simple_message()
    if response:
        return HttpResponse("Email sent!")
    else:
        return HttpResponse("Failed to send email.", status=500)