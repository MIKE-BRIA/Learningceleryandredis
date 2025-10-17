from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from a_messageboard.models import MessageBoard
from datetime import datetime


@shared_task(name='email_notification_task')
def send_email_task(subject,body,emailaddress):
    recipients = [emailaddress] if isinstance(emailaddress, str) else emailaddress
    email = EmailMessage(subject, body, to=recipients)
    email.send()
    return recipients


@shared_task(name='monthly newsletter')
def send_newsletter():
    subject = 'Your Monthly Newsletter'

    subscribers = MessageBoard.objects.get(id=1).subscribers.all()
    for subscriber in subscribers:
        body = render_to_string('a_messageboard/newsletter.html', {
            'name': subscriber.profile.name,
        })
        email = EmailMessage(subject, body, to=[subscriber.email])
        email.content_subtype = 'html'
        email.send()

    current_month = datetime.now().strftime('%B')
    return f'{current_month} Newsletter sent to {subscribers.count()} subscribers.'
