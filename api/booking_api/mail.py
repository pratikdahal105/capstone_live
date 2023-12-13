from django.core.mail import EmailMessage
from django.conf import settings
from registration.models import Token
import qrcode
from io import BytesIO

def send_booking_email(user, token):
    subject = "Your Booking Confirmation"
    message = "Here is your booking QR Code. Please bring this to the event."
    from_email = "capstone0023@gmail.com"
    recipient_list = [user.email]

    qr = qrcode.make(token)
    buffer = BytesIO()
    qr.save(buffer)
    buffer.seek(0)

    email = EmailMessage(
        subject,
        message,
        from_email,
        recipient_list
    )

    email.attach('booking_qr.png', buffer.getvalue(), 'image/png')

    email.send()
