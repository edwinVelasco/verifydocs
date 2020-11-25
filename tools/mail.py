import smtplib
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(email,subject, context, template):
    # Render and send the email template
    try:
        html_content = render_to_string(template, context)
        text_content = strip_tags(html_content)
        message = EmailMultiAlternatives(
            subject, text_content, settings.EMAIL_HOST_USER,
            email)
        message.attach_alternative(html_content, "text/html")
        message.send()
    except smtplib.SMTPException as e:
        print(e)
        raise smtplib.SMTPException(e)