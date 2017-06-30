from __future__ import unicode_literals

from django.db import models

import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validlogin(self, postData):
        email = postData["email"]
        password = postData["password"]
        errors = []

        user_list = User.objects.filter(email=email)        

        if not user_list: 
            errors.append("Invalid email and invalid password")
        else:
            user = user_list[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                    return {"status": True, "data": user_list[0]}
            else: 
                errors.append('wrong password')
        return {"status": False, "data": errors}  
        
    def validregister(self, postData):
        name = postData["name"]
        alias = postData["alias"]
        email = postData['email']
        password = postData['password']
        confirmpass = postData['confirmpass']
        birthdate = postData['birthdate']

        errors = []

        if len(name) < 1:
            errors.append("Name cannot be empty")
        elif not name.isalpha():
            errors.append("Name can only contain leters")
        
        if len(alias) < 1:
            errors.append("Name cannot be empty")
        elif not alias.isalpha():
            errors.append("Name can only contain leters")
        
        if len(email) < 1:
            errors.append("Email cannot be empty")
        elif not EMAIL_REGEX.match(email):
            errors.append("Email is not valid")
        
        if len(password) < 8:
            errors.append("Password should be at least 8 characters")
        elif password != confirmpass:
            errors.append("Password and Confirm password has to be same")
        
        if len(confirmpass) < 8:
            errors.append("Confirm password should be at least 8 characters")
        elif confirmpass != password:
            errors.append("Password and Confirm password has to be same")
        
        if not birthdate:
            errors.append("Please input your birthdate")

        
        exist = User.objects.filter(email=email).exists()

        if exist:
            errors.append("Already exists")
        
        if not errors:
            mypassword = password.encode()
            hashed = bcrypt.hashpw(mypassword,bcrypt.gensalt())
            user = User.objects.create(name=name, alias=alias, email=email, password=hashed, birthdate=birthdate)
            return {"status": True, "data": user}
        else:
            return {"status": False, "data": errors}
        
    def addFriend(self, userId, friendId):
        user = self.get(id=userId)
        friend = self.get(id=friendId)
        Friend.objects.create(friendRequest=user, acceptFriend=friend)
        Friend.objects.create(friendRequest=friend, acceptFriend=user)
    
    def removeFriend(self, userId, friendId):
        user = self.get(id=userId)
        friend = self.get(id=friendId)
        removeFriend1 = Friend.objects.get(friendRequest=user, acceptFriend=friend)
        removeFriend2 = Friend.objects.get(friendRequest=friend, acceptFriend=user)   
        removeFriend1.delete()
        removeFriend2.delete()         

class User(models.Model):
    name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    birthdate = models.DateField(blank=False, null=True)
    objects = UserManager()

class Friend(models.Model):
    friendRequest = models.ForeignKey(User, related_name="requester")
    acceptFriend = models.ForeignKey(User, related_name="accepter")
    objects = UserManager()

# Create your models here.
