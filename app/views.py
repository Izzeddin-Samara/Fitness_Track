from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
import bcrypt
from .models import User
from django.core.mail import send_mail
from django.contrib.auth import logout

def index(request):
    all_the_coaches = models.show_all_coaches(request)
    return render(request, 'home.html', {'all_the_coaches': all_the_coaches})

def login(request):
    if request.method == 'POST':
        user = models.check(request)
        if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/user_dashboard')
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

def create_session(request, coach_id):
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

    
    return render(request, 'session_form.html', {'coach': coach, 'coach_id': coach_id})

def update_session(request, session_id):
    session = models.get_session(session_id)
    coach = session.coach 

    if request.method == 'POST':
        models.update_session(request, session_id)
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
        return render(request, 'update_session.html', {'session': session, 'coach': coach})

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
    messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} deleted successfully", extra_tags='danger')
    return redirect('/upcoming_sessions')

def create_review(request, coach_id):
    coach = models.get_coach(coach_id)  

    if request.method == 'POST':
        request.session['coachid'] = coach_id
        
      
        existing_review_instance = models.existing_review(request)
        if existing_review_instance:
            messages.error(request, "You have already reviewed this coach.", extra_tags='danger')
            return redirect(f'/review/{coach_id}')
        
       
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
