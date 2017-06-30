from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages


from .models import User, Friend

def index(request):
    return render(request, 'logreg/index.html')

def friends(request):
    # if "id" in request.session:
    #     context = {
    #         "user":User.objects.get(id=request.session["id"])
    #     }
    #     return render(request, 'logreg/friends.html', context)
    # else:
    #     messages.add_message(request, messages.ERROR, "Must be a Registered User!")
    #     return redirect('/')
    selfie = User.objects.get(id=request.session['id'])
    try:
        users = User.objects.all()
        otherUsers = []
        for others in users:
            if (others.id != request.session['id']):
                otherUsers.append(others)
    except:
        users = None
    
    try: 
        friends = Friend.objects.filter(friendRequest=selfie)
        existFriends = []
        for friend in friends:
            existFriends.append(friend.acceptFriend)
        existOthers = []
        for others in otherUsers:
            if (others not in existFriends):
                existOthers.append(others)
    except:
        friends = None
    
    context = {
        'selfie': selfie,
        'users': existOthers,
        'friends': existFriends
    }
    return render(request, 'logreg/friends.html', context)

def user(request, id):
    profile = User.objects.get(id=id)
    context = {
        "user": profile
    }
    return render(request, 'logreg/user.html', context)

def login(request):
    res = User.objects.validlogin(request.POST)
    if res["status"]:
        # set id in session
        request.session["id"] = res["data"].id
        return redirect('/friends')
    
    for error in res["data"]:
        messages.error(request, error) 

    return redirect('/')


def register(request):
    res = User.objects.validregister(request.POST)
    if res["status"]:
        # set id in session
        request.session["id"] = res["data"].id
        return redirect('/friends')
    
    for error in res["data"]:
        messages.error(request, error) 

    return redirect('/')

def addfriend(request, id):
    User.objects.addFriend(request.session["id"], id)
    return redirect('/friends')

def removefriend(request, id):
    User.objects.removeFriend(request.session["id"], id)
    return redirect('/friends')

def logout(request):
    request.session.pop('id')
    return redirect('/')

# Create your views here.
