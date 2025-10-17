from django.shortcuts import redirect, render

def home_view(request):
    context = {}
    return redirect('messageboard')
