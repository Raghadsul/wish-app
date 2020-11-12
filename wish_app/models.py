from django.db import models

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if User.objects.filter(email=postData['email']).exists():
            errors["email"] = "Email address is already exists"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm_pw']:
                errors["confirm_pw"] = "Passwords should match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"] = "A wish must be at least 3 characters !"
        if len(postData['desc']) < 3:
            errors["desc"] = "A description must be at least 3 characters !"
        if len(postData['desc'].strip()) < 1:
            errors["desc"] = "A description must be provided !!"
        return errors

class Wish(models.Model):
    item = models.CharField(max_length=45)
    desc = models.CharField(max_length=255, default='')
    wished_by = models.ForeignKey(User, related_name="wishers", on_delete = models.CASCADE)
    user_who_like = models.ManyToManyField(User, related_name="liked_wishes")
    is_granded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WishManager()

