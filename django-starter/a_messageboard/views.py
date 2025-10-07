from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMessage
from .models import *
from .forms import *


# Create your views here.
@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    form = MessageCreateForm()

    if request.method == "POST":
        if request.user in messageboard.subscribers.all():
            form = MessageCreateForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.messageboard = messageboard
                message.save()
                send_email(message)

        else:
            messages.warning(request, "You must be a subscriber to post messages.")
        return redirect("messageboard")

    context = {
        "messageboard": messageboard,
        "form": form,
    }
    return render(request, "a_messageboard/index.html", context)


@login_required
def subscribe(request):
    messageboard = get_object_or_404(MessageBoard, id=1)
    if request.user in messageboard.subscribers.all():
        messageboard.subscribers.remove(request.user)
        messages.success(request, "You have unsubscribed from the message board.")
    else:
        messageboard.subscribers.add(request.user)
        messages.success(request, "You have subscribed to the message board.")
    return redirect("messageboard")


def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()

    for subscriber in subscribers:
        subject = f"New Message from {message.author.profile.name}"
        body = f"{message.author.profile.name} posted a new message:\n\n{message.body   }\n\nView the message board to reply."
        email = EmailMessage(subject, body, to=[subscriber.email])

        email.send()

        # we use threading from default python library to send email but it is slow too
        # email_thread = threading.Thread(target=send_email_thread, args=(subject, body, subscriber))
        # email_thread.start()

        # default way to send email without threading
        # def send_email_thread(subject, body, subscriber):
        #     email = EmailMessage(subject, body, to=[subscriber.email])
        #     email.send()
