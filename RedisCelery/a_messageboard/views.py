
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import MessageBoard, Message
from .forms import MessageCreateForm
from django.contrib import messages
from django.core.mail import EmailMessage
from .task import send_email_task
from django.contrib.auth.decorators import user_passes_test


# Create your views here.
@login_required
def messageboard_view(request):
    messageboard = get_object_or_404(MessageBoard, pk=1)
    form = MessageCreateForm()

    if request.method == 'POST':
        if request.user in messageboard.subscribers.all():
            form = MessageCreateForm(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.messageboard = messageboard
                message.save()
                send_email(message)
        else:
            messages.warning(request, "You must be subscribed to post messages.")
        return redirect('messageboard')

    context = {
        'messageboard': messageboard,
        'form': form,
    }
    return render(request, 'a_messageboard/index.html', context)


@login_required
def subscribe(request):
    messageboard = get_object_or_404(MessageBoard, pk=1)
    if request.user not in messageboard.subscribers.all():
        messageboard.subscribers.add(request.user)
        messages.success(request, "You have successfully subscribed to the message board.")
    else:
        messageboard.subscribers.remove(request.user)
        messages.info(request, "You have unsubscribed from the message board.")

    return redirect('messageboard')


# def send_email(message):
#     messageboard = message.messageboard
#     subscribers =  messageboard.subscribers.all()

#     for subscriber in subscribers:
#         subject = f'New message from {message.author.profile.name}'
#         body = f'{message.author.profile.name}: {message.body}\n\nVisit the message board to reply.'

#         # email = EmailMessage(subject, body, to=[subscriber.email])
#         # email.send()
#         send_email_task.delay(subject, body, subscriber.email)



# views.py or utils.py
def send_email(message):
    messageboard = message.messageboard
    subscribers = messageboard.subscribers.all()

    for subscriber in subscribers:
        subject = f'New message from {message.author.profile.name}'
        body = f'{message.author.profile.name}: {message.body}\n\nVisit the message board to reply.'
        send_email_task.delay(subject, body, subscriber.email)


def is_staff(user):
    return user.is_staff


@user_passes_test(is_staff)
def newsletter(request):
    return render(request, 'a_messageboard/newsletter.html')
