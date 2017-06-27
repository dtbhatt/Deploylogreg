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
            firstName = postData["firstName"]
            lastName = postData["lastName"]
            email = postData['email']
            password = postData['password']
            confirmpass = postData['confirmpass']
    
            errors = []

            if len(firstName) < 1:
                errors.append("Name cannot be empty")
            elif not firstName.isalpha():
                errors.append("Name can only contain leters")
            
            if len(lastName) < 1:
                errors.append("Name cannot be empty")
            elif not lastName.isalpha():
                errors.append("Name can only contain leters")
            
            if len(email) < 1:
                errors.append("Email cannot be empty")
            elif not EMAIL_REGEX.match(email):
                errors.append("Email is not valid")
            
            if len(password) < 1:
                errors.append("Password cannot be empty")
            elif password != confirmpass:
                errors.append("Password and Confirm password has to be same")
            
            if len(confirmpass) < 1:
                errors.append("Confirm password cannot be empty")
            elif confirmpass != password:
                errors.append("Password and Confirm password has to be same")
            
            
            exist = User.objects.filter(email=email).exists()

            if exist:
                errors.append("Already exists")
            
            if not errors:
                mypassword = password.encode()
                hashed = bcrypt.hashpw(mypassword,bcrypt.gensalt())
                user = User.objects.create(firstName=firstName, lastName=lastName, email=email, password=hashed)
                return {"status": True, "data": user}
            else:
                return {"status": False, "data": errors}     

class User(models.Model):
        firstName = models.CharField(max_length=45)
        lastName = models.CharField(max_length=45)
        email = models.CharField(max_length=200)
        password = models.CharField(max_length=100)
        objects = UserManager()

# Create your models here.
