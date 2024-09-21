# :muscle: FitnessTrack

## :mag_right: Overview 
FitnessTrack is a professional web application designed to connect users with certified fitness coaches to help them achieve their fitness goals. The platform allows users to browse coach profiles, book sessions, and leave reviews, all while maintaining a simple and intuitive user experience. Automated email notifications keep both users and coaches informed about session bookings, updates, and cancellations. Coaches are added to the platform by the admin, and they can log in to manage their profiles, view their schedules, and see user reviews. The platform also features a Contact Page for user support and a Coach Application Form for qualified professionals to join the platform.

## :star: Features

-  :lock: **Secure User and Coach Login**: Users can register and log in securely. Coaches, once added by an admin, can log in to access their dashboards and manage their information.

- :desktop_computer: **User Dashboard**: Users have access to a personalized dashboard where they can view their upcoming sessions, see their recent reviews, and browse available coaches, making it easier to manage their fitness journey.

- :calendar: **Simple Booking System**: Users can easily browse available coaches, book sessions that fit their needs, and manage their bookings with options to cancel or reschedule sessions.

- :pencil: **Review System**: Users can leave, update, or delete reviews for coaches, providing valuable feedback that helps maintain a high standard of coaching.

- :desktop_computer: **Coach Dashboard**: Coaches have access to a personalized dashboard where they can view upcoming sessions booked by users and see recent reviews about their services.

- :bust_in_silhouette: **Profile Management for Coaches**: Coaches can update their profiles with details such as bio, experience, education, and profile picture to attract potential clients.

- :clipboard: **Application Process for New Coaches**: Coaches who want to join FitnessTrack can submit their applications, including CVs and certifications, for admin review and approval.

- :key: **Admin Management of Coaches**: Admins add and manage coaches on the platform, controlling who can join and ensuring quality standards.

- :email: **Automated Email Notifications**: The platform send automated emails to both users and coaches when a session is booked, updated, or canceled. This keeps everyone informed about their appointments and any changes that occur.

- :envelope_with_arrow: **Contact Form for Inquiries**: Users can use a contact form to reach out for support, ask questions, or provide feedback.

## :hammer_and_wrench: Technology Stack

- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B) & ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white): Used for backend development to handle user authentication, session bookings, review systems, and overall data management. Django’s robust framework allows for secure and scalable development, ensuring smooth management of users and coaches.

- ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white): Chosen as the database to efficiently store and manage data related to users, coaches, sessions, and reviews. It ensures data integrity and supports complex queries needed for the booking and review systems.

- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black): Used to create interactive elements on the frontend, such as toggling visibility of content, managing dynamic user interactions, improving navigation, and performing client-side validation using Vanilla JavaScript to ensure forms are properly filled out before submission.

-  ![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white): A lightweight JavaScript library used to add interactivity to the frontend. Enhancing user interface elements like toggling content visibility.

- ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) & ![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white): Core technologies for structuring and styling the frontend, ensuring a clean, responsive design that enhances user experience across all devices.

- ![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white): A front-end framework that ensures the platform is mobile-friendly and visually consistent, providing a responsive design for all pages.

- ![Jazzmin](https://img.shields.io/badge/Jazzmin-FF69B4?style=for-the-badge&logo=django&logoColor=white): Customizes the Django admin interface, providing a modern and intuitive dashboard for admins to manage the platform effectively.

- ![Mailjet](https://img.shields.io/badge/Mailjet-FF6F61?style=for-the-badge&logo=mailjet&logoColor=white): Integrated for sending automated emails to users and coaches for session bookings, updates, and cancellations to ensure everyone stays informed.

- ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white): Used for version control, managing code changes, and keeping the development process organized and efficient.

## :wrench: Installation

To get started with the FitnessTrack project, follow these steps:

1. :arrow_down: **Clone the repository:**

   ```bash
   git clone https://github.com/Izzeddin-Samara/Fitness_Track.git

2. :file_folder: **Navigate to the project directory:**

   ```bash
   cd Fitness_Track

3. :package: **Create a virtual environment:**

   ```bash
   python -m venv env
4. :key: **Activate the virtual environment:**
   - On Windows
      ```bash
      call env\Scripts\activate
     
    - On MacOS/Linux
      ```bash
      source env/bin/activate
      
6. :arrow_up: **Install the required packages:**
   ```bash
   pip install -r requirements.txt

7. 💾 **Set Up MySQL Database:**

   To set up the MySQL database for the FitnessTrack project, follow the steps below. You can use MySQL Workbench, a graphical interface for managing MySQL databases.

   1. **Download and Install MySQL Workbench:**
      - If you haven't already, download and install MySQL Workbench from the [official website](https://dev.mysql.com/downloads/workbench/).

   2. **Create a New Database:**
   - Open MySQL Workbench and connect to your MySQL server.
   - In the **Navigator** pane, right-click on **Schemas** and select **Create Schema**.
   - Name the new schema `fitnesstrack` and click **Apply**.
   - Alternatively, you can run the following command in the MySQL Query window:
     ```sql
     CREATE DATABASE fitnesstrack;
     ```
     
   3. **Update `settings.py` file:**
   - Configure the database settings in `settings.py` file with the following:
     ```python
     DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'fitnesstrack', # The name of your database.
           'USER': 'your_mysql_username', # Your MySQL username.
           'PASSWORD': 'your_mysql_password', # Your MySQL password.
           'HOST': 'localhost', # The host where your MySQL database is running. Use 'localhost' if it's on your local machine.
           'PORT': '3306',  The port your MySQL server is running on. 3306 is the default MySQL port.
         }
     }
     ```
   **Notes:**

   - Ensure that your MySQL server is running, and you have the correct credentials (`your_mysql_username` and `your_mysql_password`) to access the database.
   - The database name (`fitnesstrack`) can be changed, but make sure it matches the name you set in your `settings.py`.

7. :rocket: **Run migrations to set up the database:**
     ```bash
     python manage.py makemigrations
     python manage.py migrate
8. :busts_in_silhouette: **Create a superuser:**
    - **Why?** Creating a superuser account is essential for accessing the Django admin interface, where you can manage the application's data and settings.
    - **How?** Run the following command
     ```bash
     python manage.py createsuperuser
     ```
     - **Next Steps:** Once created, you can log in through the login page at http://127.0.0.1:8000/login. Select 'Admin' from the dropdown menu to access administrative functionalities.
10. :computer: **Run the development server:**
     ```bash
     python manage.py runserver
11. :globe_with_meridians: **Open your browser and navigate to:**
      
      http://127.0.0.1:8000/

## :envelope: Email Setup

This section explains how to configure email functionalities in the FitnessTrack project. You can choose to set up Mailjet for sending real emails or Mailtrap for simulating email sending.

### :gear: Setting Up Mailjet for Real Emails

Use Mailjet if you need to send actual emails from the application

### Steps to Set Up Mailtjet:

1. **Sign Up and Get Your API Keys:**
   - Sign up for an account at [Mailjet](https://www.mailjet.com).
   - Navigate to the API section and generate your API keys (API key and Secret key).

2. **Create a `.env` File:**
   - Ensure you have a `.env` file in the project's root directory (where `manage.py` is located).

3. **Configure Mailjet in the `.env` File:**
   - Add the following lines to the `.env` file, replacing `your_value_here` with your Mailjet configuration details:
     ```plaintext
     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST='in-v3.mailjet.com'
     EMAIL_PORT=587
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER='your_mailjet_api_key'  # Replace with your actual Mailjet API key
     EMAIL_HOST_PASSWORD='your_mailjet_secret_key'  # Replace with your actual Mailjet secret key
     DEFAULT_FROM_EMAIL='your_email@example.com'  # Replace 'your_email@example.com' with the email address you registered with on Mailjet. This email will appear in the 'From' field when sending emails.
     ```

### :warning: Important Notes

- **Real Emails Required:** Mailjet requires valid email addresses for sending notifications. Ensure that you use real email addresses for users, coaches, contact forms, and coach applications to ensure successful delivery.

- **Single Email for All Notifications:** Utilize one email address (e.g., your_email@example.com) for sending all notifications to users, coaches, and via contact forms and coach applications. This simplifies the email setup and ensures compliance with Mailjet’s policy of using verified sender addresses, enhancing deliverability and consistency across your project.

## 🧪 Setting Up Mailtrap for Simulated Email Sending

Use Mailtrap if you want to simulate the process of sending emails without actual delivery. This is ideal for testing functionalities without sending real emails.

### Steps to Set Up Mailtrap:

1. **Create a Mailtrap Account:**
   - Sign up at [Mailtrap](https://mailtrap.io) and log in to your account.
   - Create an Inbox: Choose 'Email Testing', then create and configure a new inbox to receive simulated emails.
   - Obtain Credentials: After creating your inbox, locate the SMTP settings for the inbox which include the username and password. You'll need these for configuring your project's email settings.

2. **Add Mailtrap Settings to the `.env` File:**
   - Include the following settings in your `.env` file to configure Mailtrap for simulating emails:
     ```plaintext
     EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
     EMAIL_HOST='smtp.mailtrap.io'
     EMAIL_PORT=2525
     EMAIL_USE_TLS=True
     EMAIL_HOST_USER='your_mailtrap_username'  # Replace with your Mailtrap username
     EMAIL_HOST_PASSWORD='your_mailtrap_password'  # Replace with your Mailtrap password
     DEFAULT_FROM_EMAIL='your_test_email@example.com'  # Use this email for simulation purposes.
     ```

3. **Using Fake Emails for Testing:**
- Utilize fake email addresses for testing interactions with users, coaches, contact forms, and coach application forms. This ensures that all test emails are safely routed to your Mailtrap inbox. This setup allows you to review and validate email functionalities thoroughly without sending emails to real addresses.

### Note:
- By directing all test emails to your Mailtrap inbox, you can ensure the integrity of your testing process and protect real email addresses from receiving test data.
### Choosing the Right Configuration
- Use **Mailjet** if your goal is to send emails to actual recipients.
- Opt for **Mailtrap** if you are testing email functionalities and prefer not to send real emails.


