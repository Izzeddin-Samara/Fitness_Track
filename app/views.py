from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
import bcrypt
from .models import User
from django.core.mail import send_mail
from django.contrib.auth import logout
from datetime import date
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login 

def index(request):
    all_the_coaches = models.show_all_coaches(request)
    return render(request, 'home.html', {'all_the_coaches': all_the_coaches})

def login(request):
    return render(request, 'login.html')

def admin_login_view(request):  # Renamed function to avoid conflict
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  
            
            auth_login(request, user)
            return redirect('/admin/') 
        else:
            messages.error(request, "Invalid credentials or not an admin user.")
            return redirect('login_admin') 

    return render(request, 'login.html') 

def login_user(request):
    if request.method == 'POST':
        user = models.check(request)
        if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/user_dashboard')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect('login')
        
def login_coach(request):
    if request.method == 'POST':
        coach = models.get_coach_by_email(request)
        if coach and bcrypt.checkpw(request.POST['password'].encode(), coach.password.encode()):
            request.session['coach_id'] = coach.id
            return redirect('/coach_dashboard')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect('login') 
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.register_validator(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, 'register.html')

        user = models.add_user(request.POST)
        request.session['userid'] = user.id
        if user:
            return redirect('/user_dashboard')
        else:
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

def user_dashboard(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        return render(request, 'user_dashboard.html', {
            'user': user,
        })
    return redirect('/login')

def coach_dashboard(request):
    if 'coach_id' in request.session:
        coach_id = request.session['coach_id']
        coach = models.get_coach(coach_id)
        return render(request, 'coach_dashboard.html', {
            'coach': coach,
        })
    return redirect('/login')

def coach_sessions(request):
    if 'coach_id' in request.session:
        coach_id = request.session['coach_id']
        coach = models.get_coach(coach_id)
        coach_sessions = models.get_sessions_for_coach(coach_id)
        return render(request, 'coach_sessions.html', {'coach': coach, 'user_sessions': coach_sessions})

def coach_reviews(request):
    if 'coach_id' in request.session:
        coach_id = request.session['coach_id']
        coach = models.get_coach(coach_id)
        coach_reviews = models.get_reviews_for_coach(coach_id)
        return render(request, 'coach_reviews.html', {'coach': coach, 'user_reviews': coach_reviews})

def create_session(request, coach_id):
    min_date = date.today().isoformat()
    coach = models.get_coach(coach_id)

    if request.method == 'POST':
        request.session['coachid'] = coach_id
        session = models.create_session(request)
        send_mail(
            'Session Created Successfully',
            f'Your session with coach {coach.first_name} {coach.last_name} on {session.date} at {session.duration} has been successfully booked.',
            'izzidinsamara@gmail.com',  
            [session.user.email], 
            fail_silently=False,
        )
        messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} booked successfully, session details have been sent to your email", extra_tags='success')
        return redirect('/upcoming_sessions')

    
    return render(request, 'session_form.html', {'coach': coach, 'coach_id': coach_id, 'min_date': min_date})

def update_session(request, session_id):
    min_date = date.today().isoformat()
    session = models.get_session(session_id)
    coach = session.coach 

    if request.method == 'POST':
        models.update_session(request, session_id)

        session.refresh_from_db()
        
        send_mail(
            'Session Updated Successfully',
            f'Your session with coach {coach.first_name} {coach.last_name} has been updated to be on {session.date} at {session.duration} at {session.place} .',
            'izzidinsamara@gmail.com',
            [session.user.email],
            fail_silently=False,
        )
        messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        return redirect('/upcoming_sessions')
    else:
        return render(request, 'update_session.html', {'session': session, 'coach': coach, 'min_date': min_date})

def cancel_session(request, session_id):
    session = models.get_session(session_id)
    coach = session.coach
    models.delete_session(session_id)
    send_mail(
        'Session Deleted Successfully',
        f'Your session with coach {coach.first_name} {coach.last_name} on {session.date} at {session.duration}  has been successfully cancelled.',
        'izzidinsamara@gmail.com',
        [session.user.email],
        fail_silently=False,
    )
    messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} cancelled successfully", extra_tags='success')
    return redirect('/upcoming_sessions')

def create_review(request, coach_id):
    coach = models.get_coach(coach_id)  

    if request.method == 'POST':
        request.session['coachid'] = coach_id
        
      
        existing_review_instance = models.existing_review(request)
        if existing_review_instance:
            messages.error(request, "You have already reviewed this coach.", extra_tags='danger')
            return redirect(f'/create_review/{coach_id}')
        
       
        models.add_review(request)
        messages.success(request, f"Review submitted successfully for coach {coach.first_name} {coach.last_name}", extra_tags='success')
        return redirect('/recent_reviews')

    return render(request, 'review_form.html', {'coach': coach, 'coach_id': coach_id})

def update_review(request, review_id):
    review = models.get_review(review_id)
    coach = review.coach  

    if request.method == 'POST':
        models.update_review(request, review_id)
        messages.success(request, f" Review for coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        return redirect('/recent_reviews')
    else:
        return render(request, 'update_review.html', {'review': review, 'coach': coach})

def delete_review(request, review_id):
    review = models.get_review(review_id)
    models.delete_review(review_id)
    coach = review.coach    
    messages.success(request, f" Review for coach {coach.first_name} {coach.last_name} deleted successfully.", extra_tags='success')
    return redirect('/recent_reviews', {'review' : review, 'coach' : coach})

def logout_user(request):
    logout(request)
    return redirect('/')

def about_us(request):
    return render(request, 'about_us.html')

def terms(request):
    return render(request, 'terms.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def upcoming_sessions(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        user_sessions = models.get_sessions_by_user(user_id)
        return render(request, 'upcoming_sessions.html', {'user': user, 'user_sessions': user_sessions})

def recent_reviews(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        user_reviews = models.get_reviews_by_user(user_id)
        return render(request, 'recent_reviews.html', {'user': user, 'user_reviews': user_reviews})

def available_coaches(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
    coaches = models.show_all_coaches(request)
    return render(request, 'available_coaches.html', {'user': user, 'coaches': coaches})

def contact(request):
    return render(request, 'contact.html')

def add_contact(request):
    if request.method == 'POST':
        print(request.POST)  # Check the incoming data
        contact = models.add_contact(request)
        if contact:
            send_confirmation_email(contact)
            messages.success(request, f"Your message submitted successfully!", extra_tags='success')
            return redirect('/contact')
        else:
            return render(request, 'contact.html', {'error': 'Failed to create contact'})
    return render(request, 'contact.html')

def send_confirmation_email(contact):
    subject = 'We Have Received Your Contact Request'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [contact.email]

    email_body = (
        f"Dear {contact.name},\n\n"
        "Thank you for reaching out to us. We have received your message and our team will "
        "get in touch with you shortly. We appreciate your patience and look forward to assisting you.\n\n"
        "Best regards,\n"
        "FitnessTrack Team\n"
    )

    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email=from_email,
        to=recipient_list
    )
    email.send()

def coach_application(request):
    if request.method == 'POST':
        # Call the model function with POST and FILES data
        application = models.submit_application(request.POST, request.FILES)

        # Prepare the email
        email = EmailMessage(
            subject='New Coach Application Received',
            body=f"New coach application submitted by {request.POST.get('first_name')} {request.POST.get('last_name')}. Please find the attached documents.",
            from_email=settings.DEFAULT_FROM_EMAIL,  # Ensure you have set this in your settings
            to=['izzidinsamara@gmail.com'],  # Replace with your email
        )

        # Attach files to the email
        for file in request.FILES.values():
            email.attach(file.name, file.read(), file.content_type)

        # Send the email
        email.send()

        # Render success template
        return render(request, 'success.html', {'application': application})
    else:
        # In case of a GET request, render the application form
        return render(request, 'coach_application.html')

def coach_profile(request, coach_id):
    coach = models.get_coach(coach_id)
    coach_expereices = models.coach_experience(coach_id)
    coach_eduction = models.coach_education(coach_id)

    # Pass 'user' in the context
    return render(request, 'coach_profile.html', {
        'coach': coach,
        'coach_expereinces': coach_expereices,
        'coach_education': coach_eduction,
        'user': request.user  # Explicitly pass the user object
    })

def add_experience(request, coach_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    if logged_in_coach_id != coach_id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    coach = models.get_coach(coach_id)
    
    if request.method == 'POST':
        models.add_experience(request)
        return redirect('coach_profile', coach_id=coach_id)
    
    context = {
        'coach': coach
    }
    
    return render(request, "experience_form.html", context)

def update_experience(request, experience_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    experience = models.get_experience(experience_id)
    coach = experience.coach

    if logged_in_coach_id != coach.id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    if request.method == 'POST':
        models.update_experience(request, experience_id)
        messages.success(request, f"Experience for coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        return redirect('coach_profile', coach_id=logged_in_coach_id)
    else:
        return render(request, 'update_experience.html', {'experience': experience, 'coach': coach, 'coach_id': logged_in_coach_id})

def delete_experience(request, experience_id):
    
    if 'coach_id' not in request.session:
        return redirect('login')  

    logged_in_coach_id = request.session['coach_id']
    
    
    experience = models.get_experience(experience_id)
    coach = experience.coach

    
    if logged_in_coach_id != coach.id:
        messages.error(request, "You are not authorized to delete this experience.")
        return redirect('coach_profile', coach_id=logged_in_coach_id)  

    
    models.delete_experience(experience_id)
    messages.success(request, "Experience deleted successfully.")
    
    
    return redirect('coach_profile', coach_id=logged_in_coach_id)

def add_education(request, coach_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    if logged_in_coach_id != coach_id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    coach = models.get_coach(coach_id)
    
    if request.method == 'POST':
        models.add_education(request)
        return redirect('coach_profile', coach_id=coach_id)
    
    context = {
        'coach': coach
    }
    
    return render(request, "education_form.html", context)

def update_education(request, education_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    education = models.get_education(education_id)
    coach = education.coach

    if logged_in_coach_id != coach.id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    if request.method == 'POST':
        models.update_education(request, education_id)
        messages.success(request, f"Education for coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        return redirect('coach_profile', coach_id=logged_in_coach_id)
    else:
        return render(request, 'update_education.html', {'education': education, 'coach': coach, 'coach_id': logged_in_coach_id})