from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User

def index(request):
    return render(request, 'logreg/index.html')

def success(request):
    if "id" in request.session:
        context = {
            "user":User.objects.get(id=request.session["id"]),
            "users":User.objects.all()
        }
        return render(request, 'logreg/success.html', context)
    else:
        messages.add_message(request, messages.ERROR, "Must be a Registered User!")
        return redirect('/')

def login(request):
    res = User.objects.validlogin(request.POST)
    if res["status"]:
        # set id in session
        request.session["id"] = res["data"].id
        return redirect('/success')
    
    for error in res["data"]:
        messages.error(request, error) 

    return redirect('/')


def register(request):
    res = User.objects.validregister(request.POST)
    if res["status"]:
        # set id in session
        request.session["id"] = res["data"].id
        return redirect('/success')
    
    for error in res["data"]:
        messages.error(request, error) 

    return redirect('/')

def newpoke(request, id):
    poke = Poke.objects.newpoke(id, request.session['id'])
    return redirect('/success')

def logout(request):
    request.session.pop('id')
    return redirect('/')

# Create your views here.
