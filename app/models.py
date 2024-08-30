from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData, user_id=None):
        errors = {}
        email_check = User.objects.filter(email=postData['email'])
        if user_id:
            email_check = email_check.exclude(id=user_id)
        if email_check.exists():
            errors["email"] = "Email must be unique"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_error'] = "Invalid email!"
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['password_confirmation']:
            errors["password_confirmation"] = "Passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Coach(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Session(models.Model):
    coach = models.ForeignKey(Coach, related_name= "coach_sessions", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_sessions", on_delete=models.CASCADE)
    date = models.DateField()
    duration = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    coach = models.ForeignKey(Coach, related_name= "coach_reviews",  on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name= "user_reviews", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def add_user(postData):
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    password = postData['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
    return user

def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user

def check(request):
    return User.objects.filter(email=request.POST['email']).first()

def get_coach(coach_id):
    return Coach.objects.get(id=coach_id)

def show_all_coaches(request):
    return Coach.objects.all()
