from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.celery import app


@app.task()
def send_email_confirmation_link_task(
    user_email: str, first_name: str, last_name: str, verification_link: str
):
    template = "users/email/confirm_email.html"
    title = "Email verification"

    html_message = render_to_string(
        template,
        {
            "first_name": first_name,
            "last_name": last_name,
            "verification_link": verification_link,
        },
    )

    message = EmailMessage(title, html_message, to=[user_email])
    message.content_subtype = "html"
    message.send()
