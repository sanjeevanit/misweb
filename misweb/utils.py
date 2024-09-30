from twilio.rest import Client
from django.conf import settings

def send_sms_via_twilio(to, message):
    # Check if the phone number starts with '+' (indicating it already has the country code)
    if not to.startswith('+'):
        # If not, prepend the country code (assuming +91 for India, you might need to adjust accordingly)
        to = '+94' + to

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )

    if message.error_code is None:
        print("Message sent successfully.")
        return True
    else:
        print(f"Message failed with error: {message.error_message}")
        return False
