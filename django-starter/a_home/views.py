from django.shortcuts import render
from django.shortcuts import redirect


def home_view(request):
    context = {}
    # return render(request, 'home.html', context)
    return redirect("messageboard")
