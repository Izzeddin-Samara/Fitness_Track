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
import os

# Renders the home page with a list of all coaches.
def index(request):
    all_the_coaches = models.show_all_coaches(request)
    return render(request, 'home.html', {'all_the_coaches': all_the_coaches})

# Renders the login page.
def login(request):
    return render(request, 'login.html')

# Handles the login process for admin users.
# Authenticates the user and redirects to the admin dashboard if credentials are valid.
def admin_login_view(request):
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

# Handles the login process for regular users.
# Validates credentials and redirects to the user dashboard on success.
def login_user(request):
    if request.method == 'POST':
        user = models.check(request)
        if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['userid'] = user.id
            return redirect('/user_dashboard')
        else:
            messages.error(request, "Invalid email or password", extra_tags='login')
            return redirect('login')
        
# Handles the login process for coaches.
# Validates credentials and redirects to the coach dashboard on success.
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

# Handles the user registration process.
# Validates input and creates a new user, then redirects to the user dashboard.
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

# Renders the user dashboard.
# Provides navigation options for users to view recent reviews, upcoming sessions, and explore available coaches.
def user_dashboard(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        return render(request, 'user_dashboard.html', {
            'user': user,
        })
    return redirect('/login')

# Renders the coach dashboard.
# Provides navigation options for coaches to access their recent reviews, upcoming sessions, and profile management.
def coach_dashboard(request):
    if 'coach_id' in request.session:
        coach_id = request.session['coach_id']
        coach = models.get_coach(coach_id)
        return render(request, 'coach_dashboard.html', {
            'coach': coach,
        })
    return redirect('/login')

# Renders the coach sessions page.
# Displays a list of sessions for the logged-in coach.
def coach_sessions(request):
    if 'coach_id' in request.session:
        coach_id = request.session['coach_id']
        coach = models.get_coach(coach_id)
        coach_sessions = models.get_sessions_for_coach(coach_id)
        return render(request, 'coach_sessions.html', {'coach': coach, 'user_sessions': coach_sessions})

# Renders the coach reviews page.
# Displays reviews for a specific coach.
def coach_reviews(request, coach_id):
    coach = models.get_coach(coach_id)
    coach_reviews = models.get_reviews_for_coach(coach_id)
    is_coach = 'coach_id' in request.session and request.session['coach_id'] == coach_id
    return render(request, 'coach_reviews.html', {
        'coach': coach,
        'coach_reviews': coach_reviews,
        'is_coach': is_coach,
    })

# Checks if the required email settings are configured in environment variables.
# Returns True if all required settings are available, else False.
def is_email_configured():
    required_settings = [
        os.environ.get('DEFAULT_FROM_EMAIL'),
        os.environ.get('EMAIL_HOST_USER'),
        os.environ.get('EMAIL_HOST_PASSWORD'),
    ]
    return all(required_settings)

# Handles the creation of a new session.
# Allows users to book a session with a specific coach and sends email notifications if email settings are configured.
# If email settings are missing, a warning message is displayed, and the session is created without sending emails.
def create_session(request, coach_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    min_date = date.today().isoformat()
    coach = models.get_coach(coach_id)

    if request.method == 'POST':
        request.session['coachid'] = coach_id
        session = models.create_session(request)

        if session:
             if is_email_configured():
                send_mail(
                'Session Created Successfully',
                f'Your session with coach {coach.first_name} {coach.last_name} on {session.date} at {session.duration} has been successfully booked.',
                os.environ.get('DEFAULT_FROM_EMAIL'),
                [session.user.email],
                fail_silently=False,
                )

                send_mail(
                'New Session Booked',
                f'A new session has been booked by {user.first_name} {user.last_name} on {session.date} at {session.duration}. Please check your dashboard for more details.',
                os.environ.get('DEFAULT_FROM_EMAIL'),
                [session.coach.email],
                fail_silently=False,
                )
                messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} booked successfully. Session details have been sent to your email.", extra_tags='success')
             else:
                  messages.warning(request, f"Session booked successfully with coach {coach.first_name} {coach.last_name}. However, we couldn’t send a confirmation email due to missing email settings.")

        return redirect('/user_sessions')

    return render(request, 'session_form.html', {'user': user, 'coach': coach, 'coach_id': coach_id, 'min_date': min_date})

# Handles the update of an existing session.
# Allows users to update session details and sends email notifications if email settings are configured.
# If email settings are missing, a warning message is displayed, and the session is updated without sending emails.
def update_session(request, session_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    min_date = date.today().isoformat()
    session = models.get_session(session_id)
    coach = session.coach

    if request.method == 'POST':
        models.update_session(request, session_id)

        if is_email_configured():
            session.refresh_from_db()
            send_mail(
                'Session Updated Successfully',
                f'Your session with coach {coach.first_name} {coach.last_name} has been updated to be on {session.date} at {session.duration} at {session.place}.',
                os.environ.get('DEFAULT_FROM_EMAIL'),
                [session.user.email],
                fail_silently=False,
            )

            send_mail(
                'Session Updated',
                f'The session booked by {user.first_name} {user.last_name} has been updated to be on {session.date} at {session.duration} at {session.place}. Please check your dashboard for more details.',
                os.environ.get('DEFAULT_FROM_EMAIL'),
                [session.coach.email],
                fail_silently=False,
            )

            messages.success(request, f"Session with coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        else:
            messages.warning(request, f"Session with coach {coach.first_name} {coach.last_name} updated successfully. However, we couldn’t send an update confirmation email due to missing email settings.")
        
        return redirect('/user_sessions')

    return render(request, 'update_session.html', {'user': user, 'session': session, 'coach': coach, 'min_date': min_date})


# Handles the cancellation of a session.
# Cancel the session and sends email notifications to the user and coach if email settings are configured.
# If email settings are missing, a warning message is displayed, and the session is canceled without sending emails.
def cancel_session(request, session_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    session = models.get_session(session_id)
    coach = session.coach

    models.delete_session(session_id)

    if is_email_configured():
        send_mail(
            'Session Cancelled Successfully',
            f'Your session with coach {coach.first_name} {coach.last_name} on {session.date} at {session.duration} has been successfully cancelled.',
            os.environ.get('DEFAULT_FROM_EMAIL'),
            [session.user.email],
            fail_silently=False,
        )

        send_mail(
            'Session Cancelled',
            f'The session booked by {user.first_name} {user.last_name} on {session.date} at {session.duration} has been cancelled.',
            os.environ.get('DEFAULT_FROM_EMAIL'),
            [session.coach.email],
            fail_silently=False,
        )

        messages.success(
            request,
            f"Session with coach {coach.first_name} {coach.last_name} cancelled successfully. Notification email has been sent.",
            extra_tags='success'
        )
    else:
        messages.warning(
            request,
            f"Session with coach {coach.first_name} {coach.last_name} cancelled successfully. However, we couldn’t send a confirmation email due to missing email settings."
        )

    return redirect('/user_sessions')


# Handles the creation of a new review for a coach.
# Allows users to submit a review and ensures that duplicate reviews are not allowed.
def create_review(request, coach_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    coach = models.get_coach(coach_id)  

    if request.method == 'POST':
        request.session['coachid'] = coach_id

        existing_review_instance = models.existing_review(request)
        if existing_review_instance:
            messages.error(request, "You have already reviewed this coach.", extra_tags='danger')
            return redirect(f'/create_review/{coach_id}')

        models.add_review(request)
        messages.success(request, f"Review submitted successfully for coach {coach.first_name} {coach.last_name}", extra_tags='success')
        return redirect('/user_reviews')

    return render(request, 'review_form.html', {'user': user, 'coach': coach, 'coach_id': coach_id})

# Handles the update of an existing review.
# Allows users to update their review for a coach.
def update_review(request, review_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    review = models.get_review(review_id)
    coach = review.coach  

    if request.method == 'POST':
        models.update_review(request, review_id)
        messages.success(request, f" Review for coach {coach.first_name} {coach.last_name} updated successfully.", extra_tags='info')
        return redirect('/user_reviews')
    else:
        return render(request, 'update_review.html', {'review': review, 'coach': coach})

# Handles the deletion of a review.
# Deletes the review and displays a success message.
def delete_review(request, review_id):
    if 'userid' not in request.session:
        return redirect('login')

    user_id = request.session['userid']
    user = models.get_user(user_id)
    review = models.get_review(review_id)
    models.delete_review(review_id)
    coach = review.coach    
    messages.success(request, f" Review for coach {coach.first_name} {coach.last_name} deleted successfully.", extra_tags='success')
    return redirect('/user_reviews', {'review' : review, 'coach' : coach})

# Logs out the user and redirects to the home page.
def logout_user(request):
    logout(request)
    return redirect('/')

# Renders the About Us page.
def about_us(request):
    return render(request, 'about_us.html')

# Renders the Terms of Service page.
def terms(request):
    return render(request, 'terms.html')

# Renders the Privacy Policy page.
def privacy_policy(request):
    return render(request, 'privacy_policy.html')

# Renders the upcoming sessions page.
# Displays a list of upcoming sessions for the logged-in user.
def user_sessions(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        user_sessions = models.get_sessions_by_user(user_id)
        return render(request, 'user_sessions.html', {'user': user, 'user_sessions': user_sessions})

# Renders the recent reviews page.
# Displays a list of recent reviews for the logged-in user.
def user_reviews(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
        user_reviews = models.get_reviews_by_user(user_id)
        return render(request, 'user_reviews.html', {'user': user, 'user_reviews': user_reviews})

# Renders the available coaches page.
# Displays a list of all available coaches.
def available_coaches(request):
    if 'userid' in request.session:
        user_id = request.session['userid']
        user = models.get_user(user_id)
    coaches = models.show_all_coaches(request)
    return render(request, 'available_coaches.html', {'user': user, 'coaches': coaches})

# Renders the contact page.
def contact(request):
    return render(request, 'contact.html')

# Handles the submission of the contact form.
# Sends a confirmation email to the user and an alert email to the admin if email settings are configured.
# If email settings are missing, a warning message is displayed, and the contact message is processed without sending emails.
def add_contact(request):
    if request.method == 'POST':
        print(request.POST)  
        contact = models.add_contact(request)
        
        if contact:
            if is_email_configured():
                send_confirmation_email(contact)
                send_admin_email(contact)
                messages.success(request, "Message sent successfully. A confirmation email has been sent.", extra_tags='success')
            else:
                messages.warning(request, "Message sent successfully. However, we couldn’t send a confirmation email due to missing email settings.")
            return redirect('/contact')
        else:
            return render(request, 'contact.html', {'error': 'Failed to create contact'})
    
    return render(request, 'contact.html')


# Sends a confirmation email to the user after submitting the contact form.
def send_confirmation_email(contact):
    subject = 'We Have Received Your Contact Request'
    from_email = os.environ.get('DEFAULT_FROM_EMAIL')
    recipient_list = [contact.email]

    email_body = (
        f"Dear {contact.name},\n\n"
        "Thank you for reaching out to us. We have received your message and our team will "
        "get in touch with you shortly. We appreciate your patience and look forward to assisting you.\n\n"
        "Best regards,\n"
        "FitnessTrack Team\n"
    )

    email = EmailMessage (
        subject=subject,
        body=email_body,
        from_email=from_email,
        to=recipient_list
    )
    email.send()

# Sends an email to the admin with the details of the contact form submission.
def send_admin_email(contact):
    subject = 'New Contact Message'
    from_email = os.environ.get('DEFAULT_FROM_EMAIL')
    recipient_list = [os.environ.get('DEFAULT_FROM_EMAIL')]

    email_body = (
        f"New contact request received from {contact.name}.\n\n"
        f"Email: {contact.email}\n"
        f"Message: {contact.message}\n\n"
        "Please follow up with this contact as soon as possible.\n\n"
    )

    email = EmailMessage (
        subject=subject,
        body=email_body,
        from_email=from_email,
        to=recipient_list
    )
    email.send()

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB in bytes

ALLOWED_FILE_TYPES = [
    'application/pdf',  # PDF files
    'image/jpeg',       # JPEG image files
    'application/msword',  # DOC files
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # DOCX files
]

# Handles the coach application process.
# Validates and processes the application form, then sends notification emails to the admin and the applicant if email settings are configured.
# If email settings are missing, a warning message is displayed, and the application is processed without sending emails.
def coach_application(request):
    if request.method == 'POST':
        application = models.submit_application(request.POST, request.FILES)
        email_warning = not is_email_configured()

        if not email_warning:
            admin_email = EmailMessage(
                subject='New Coach Application Received',
                body=f"New coach application submitted by {request.POST.get('first_name')} {request.POST.get('last_name')}. Please find the attached documents.",
                from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                to=[os.environ.get('DEFAULT_FROM_EMAIL')],
            )

            
            skipped_files = []
            for file_key, file in request.FILES.items():
                if file.size <= MAX_FILE_SIZE and file.content_type in ALLOWED_FILE_TYPES:
                    file.seek(0)
                    file_content = file.read()
                    if file_content:
                        admin_email.attach(file.name, file_content, file.content_type)
                else:
                    skipped_files.append(file.name)

            
            if admin_email.attachments:
                admin_email.send()

            applicant_email = EmailMessage(
                subject='Your Coach Application Has Been Submitted',
                body=f"Dear {request.POST.get('first_name')},\n\nThank you for submitting your application as a coach. We have received your application and will review it soon.\n\nBest regards,\nFitnessTrack Team",
                from_email=os.environ.get('DEFAULT_FROM_EMAIL'),
                to=[request.POST.get('email')],
            )
            applicant_email.send()
            messages.success(request, "Application submitted successfully. Notification emails have been sent.")
        else:
            messages.warning(request, "Application submitted successfully. However, we couldn’t send notification emails due to missing email settings.")

        return redirect('coach_application') 

    return render(request, 'coach_application.html')

# Renders the coach profile page.
# Displays the coach's information, experiences, and education.
def coach_profile(request, coach_id):
    coach = models.get_coach(coach_id)
    coach_experiences = models.coach_experience(coach_id)
    coach_education = models.coach_education(coach_id)
    is_coach = 'coach_id' in request.session and request.session['coach_id'] == coach_id
    is_logged_in = 'userid' in request.session or is_coach
    return render(request, 'coach_profile.html', {
        'coach': coach,
        'coach_experiences': coach_experiences,
        'coach_education': coach_education,
        'is_coach': is_coach,
        'is_logged_in': is_logged_in,
    })

# Handles the addition of a new experience for the coach.
# Allows the coach to add experiences to their profile.
def add_experience(request, coach_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    if logged_in_coach_id != coach_id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    coach = models.get_coach(coach_id)
    
    if request.method == 'POST':
        models.add_experience(request)
        messages.success(request, f"Experience Added successfully.", extra_tags='success')
        return redirect('coach_profile', coach_id=coach_id)
    
    context = {
        'coach': coach
    }
    
    return render(request, "experience_form.html", context)

# Handles the update of an existing experience for the coach.
# Allows the coach to update their experiences on their profile.
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
        messages.success(request, f"Experience updated successfully.", extra_tags='info')
        return redirect('coach_profile', coach_id=logged_in_coach_id)
    else:
        return render(request, 'update_experience.html', {'experience': experience, 'coach': coach, 'coach_id': logged_in_coach_id})

# Handles the deletion of an experience.
# Allows the coach to delete an experience from their profile.
def delete_experience(request, experience_id):
    if 'coach_id' not in request.session:
        return redirect('login')  

    logged_in_coach_id = request.session['coach_id']
    experience = models.get_experience(experience_id)
    coach = experience.coach

    if logged_in_coach_id != coach.id:
        messages.error(request, "You are not authorized to delete this experience.", extra_tags='success')
        return redirect('coach_profile', coach_id=logged_in_coach_id)  

    models.delete_experience(experience_id)
    messages.success(request, "Experience deleted successfully.")
    
    return redirect('coach_profile', coach_id=logged_in_coach_id)

# Handles the addition of a new education entry for the coach.
# Allows the coach to add educational qualifications to their profile.
def add_education(request, coach_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    if logged_in_coach_id != int(coach_id):  # Ensure types are consistent
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    coach = models.get_coach(coach_id)

    if request.method == 'POST':
        models.add_education(request)
        messages.success(request, "Education Added successfully.", extra_tags='success')
        return redirect('coach_profile', coach_id=coach_id)
    else:
        # Assume there is a form for GET requests to add education
        return render(request, 'education_form.html', {'coach': coach})

# Handles the update of an existing education entry for the coach.
# Allows the coach to update their educational qualifications on their profile.
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
        messages.success(request, f"Education updated successfully.", extra_tags='info')
        return redirect('coach_profile', coach_id=logged_in_coach_id)
    else:
        return render(request, 'update_education.html', {'education': education, 'coach': coach, 'coach_id': logged_in_coach_id})

# Handles the deletion of an education entry.
# Allows the coach to delete an educational qualification from their profile.
def delete_education(request, education_id):
    if 'coach_id' not in request.session:
        return redirect('login')  

    logged_in_coach_id = request.session['coach_id']
    education = models.get_education(education_id)
    coach = education.coach

    if logged_in_coach_id != coach.id:
        messages.error(request, "You are not authorized to delete this education.")
        return redirect('coach_profile', coach_id=logged_in_coach_id)  

    models.delete_education(education_id)
    messages.success(request, "Education deleted successfully.", extra_tags='success')
    
    return redirect('coach_profile', coach_id=logged_in_coach_id)

# Handles the update of the coach's bio.
# Allows the coach to update their bio on their profile.
def update_bio(request, coach_id):
    if 'coach_id' not in request.session:
        return redirect('login')

    logged_in_coach_id = request.session['coach_id']
    coach = models.get_coach(coach_id)

    if logged_in_coach_id != coach.id:
        return redirect('coach_profile', coach_id=logged_in_coach_id)

    if request.method == 'POST':
        models.update_bio(request, coach_id)
        messages.success(request, "Bio updated successfully.", extra_tags='info')
        return redirect('coach_profile', coach_id=logged_in_coach_id)
    else:
        return render(request, 'update_bio.html', {'coach': coach, 'coach_id': logged_in_coach_id})
    
# Handles the update of the coach's profile image.
# Allows the coach to update their profile image.
def update_image(request, coach_id):
    coach = models.get_coach(coach_id)

    if request.method == 'POST' and 'image' in request.FILES:
        image = request.FILES.get('image')
        if image:  
            coach.image = image
            coach.save()
            messages.success(request, "Profile image updated successfully.")
        else:
            messages.error(request, "Please upload a valid image.")
        
        return redirect('coach_profile', coach_id=coach.id)

    messages.error(request, "Invalid request to update image.")
    return redirect('coach_profile', coach_id=coach.id)