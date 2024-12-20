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
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CoachApplication(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    cv = models.FileField(upload_to='cvs/')
    certificates = models.FileField(upload_to='certificates/')
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

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Experience(models.Model):
    coach = models.ForeignKey(Coach, related_name= "coach_experiences", on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    date_range = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Education(models.Model):
    coach = models.ForeignKey(Coach, related_name= "coach_educations", on_delete=models.CASCADE)
    field_of_study = models.CharField(max_length=50) 
    degree = models.CharField(max_length=50)
    university_name = models.CharField(max_length=50)
    date_range = models.CharField(max_length=50)
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

def get_coach_by_email(request):
    return Coach.objects.filter(email=request.POST['email']).first()

def get_coach(coach_id):
    return Coach.objects.get(id=coach_id)

def show_all_coaches(request):
    return Coach.objects.all()

def create_session(request):
    user_id = request.session['userid']
    coach_id = request.session['coachid']
    date = request.POST['date']
    duration = request.POST['duration']
    place =request.POST['place']
    user = User.objects.get(id=user_id)
    coach = Coach.objects.get(id=coach_id)
    session = Session.objects.create(date=date, duration=duration, user=user, coach=coach, place=place)
    return session

def update_session(request, session_id): 
    session = Session.objects.get(id=session_id)
    session.date = request.POST['date']
    session.duration= request.POST['duration']
    session.place=request.POST['place']
    session.save()

def delete_session(session_id):
    session = Session.objects.get(id=session_id)
    session.delete()
    return session

def get_session(session_id):
    session = Session.objects.get(id=session_id)
    return session

def add_review(request):
    user_id = request.session['userid']
    coach_id = request.session['coachid']
    content = request.POST['content']
    user = User.objects.get(id=user_id)
    coach = Coach.objects.get(id=coach_id)
    review = Review.objects.create(content=content, user=user, coach=coach)
    return review

def existing_review(request):
    user_id = request.session['userid']
    coach_id = request.session['coachid']
    user = User.objects.get(id=user_id)
    coach = Coach.objects.get(id=coach_id)
    return Review.objects.filter(coach=coach, user=user).first()

def update_review(request, review_id): 
    review = Review.objects.get(id=review_id)
    review.content = request.POST['content']
    review.save()

def delete_review(review_id):
    review = Review.objects.get(id=review_id)
    review.delete()
    return review

def get_review(review_id):
    review = Review.objects.get(id=review_id)
    return review

def get_reviews_by_user(user_id):
    return Review.objects.filter(user__id=user_id)

def get_sessions_by_user(user_id):
    return Session.objects.filter(user__id=user_id)

def get_sessions_for_coach(coach_id):
    return Session.objects.filter(coach__id=coach_id)

def get_reviews_for_coach(coach_id):
    return Review.objects.filter(coach__id=coach_id)

def add_contact(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']
    contact = Contact.objects.create(name=name,email=email,message=message)
    return contact

def submit_application(postData, fileData):
    first_name = postData['first_name']
    last_name = postData['last_name']
    email = postData['email']
    address = postData['address']
    phone_number = postData['phone_number']
    certificates = fileData['certificates']
    cv = fileData['cv']
    
    
    application = CoachApplication.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
        address=address,
        certificates=certificates,
        cv=cv
    )
    return application

def coach_education(coach_id):
    return Education.objects.filter(coach__id=coach_id)
def coach_experience(coach_id):
    return Experience.objects.filter(coach__id=coach_id)

def add_experience(request):
    coach_id = request.session.get('coach_id')
    coach = get_coach(coach_id)
    job_title = request.POST['job_title']
    institution_name = request.POST['institution_name']
    date_range = request.POST['date_range']
    description = request.POST['description']
    experience = Experience.objects.create(coach=coach, job_title=job_title, institution_name=institution_name,date_range=date_range, description=description)
    return experience

def update_experience(request, experience_id):
    experience = Experience.objects.get(id=experience_id)

    experience.job_title = request.POST['job_title']
    experience.institution_name = request.POST['institution_name']
    experience.date_range = request.POST['date_range']
    experience.description = request.POST['description']
    experience.save()

    return experience


def get_experience(experience_id):
    experience = Experience.objects.get(id=experience_id)
    return experience

def delete_experience(experience_id):
    experience = Experience.objects.get(id=experience_id)
    experience.delete()

def add_education(request):
    coach_id = request.session.get('coach_id')
    coach = get_coach(coach_id)
    field_of_study = request.POST['field_of_study']
    degree = request.POST['degree']
    university_name = request.POST['university_name']
    date_range = request.POST['date_range']
    education = Education.objects.create(coach=coach, field_of_study=field_of_study, degree=degree, university_name=university_name, date_range=date_range)
    return education

def update_education(request, education_id):  
    education = Education.objects.get(id=education_id)

    education.field_of_study = request.POST['field_of_study']
    education.degree = request.POST['degree']
    education.university_name = request.POST['university_name']
    education.date_range = request.POST['date_range']
   
    education.save()

    return education

def get_education(education_id):
    education = Education.objects.get(id=education_id)
    return education

def delete_education(education_id):
    education = Education.objects.get(id=education_id)
    education.delete()

def update_bio(request, coach_id):
    coach = get_coach(coach_id)
    coach.bio = request.POST['bio']
    coach.save()

    return coach


def update_image(self, image_file):
        """Update the coach's profile image."""
        self.image = image_file
        self.save()
