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

## 📧 Email Setup

For detailed instructions on setting up email notifications in FitnessTrack, please refer to the [Email Setup Guide](https://github.com/Izzeddin-Samara/Fitness_Track/wiki/Email-Setup).

## 📘 Usage

This section includes video guides that detail the functionalities of the application. These tutorials are intended to assist users in navigating and utilizing the platform effectively.

### Video Guides

### 🧍 General User Interaction
- **Description**: Get started with basic functionalities available to all users.
##### 🎥 User Login and Registration
- **Description**: Watch how users can easily login and register on the platform.
- **Link to Video**: [User Login and Registration](https://drive.google.com/file/d/1mP8i_xBf8x3296GwS7nz18Se31KoJ7W5/view?usp=sharing)

##### 🎥 Contact Form
- **Description**: This guide demonstrates how to use the contact form for suggestions, feedback, or support.
- **Link to Video**: [Contact Us Form](https://drive.google.com/file/d/14hkvlAU3IW6Bvndmv3xfXCtX6_ZicMAJ/view?usp=sharing)

##### 🎥 Booking Management
- **Description**: Explore the process for managing bookings, including how to book, update, and cancel them.
- **Link to Video**: [Booking Management](https://drive.google.com/file/d/1sg0IgHLmc2UcHfsAdbski-luQkJJu_nh/view?usp=sharing)

##### 🎥 Managing Reviews
- **Description**: Understand how to oversee reviews on the platform, including how to post, update, or delete them.
- **Link to Video**: [Managing Reviews](https://drive.google.com/file/d/1DNmiO_YIL0DCJlTfJJKnB0NQhmBe-4Zb/view?usp=sharing)

### 🏋️ Coach-Specific Features
- **Description**: Features and functionalities specific to coaches on the platform.
##### 🎥 Coach Application
- **Description**: Learn how prospective coaches can apply to join our team through the application form.
- **Link to Video**: [Coach Application](https://drive.google.com/file/d/1qAY6GpZfB-8Wj8S3PC2vj0xWxjvMLPaz/view?usp=sharing)

##### 🎥 Coach Login
- **Description**: Discover how coaches log in and access their recent reviews and upcoming sessions.
- **Link to Video**: [Coach Login](https://drive.google.com/file/d/1irLxebJy5McTS670IR_vq2ZLfX1DJlic/view?usp=sharing)

##### 🎥 Coach Profile Management
- **Description**: Learn how coaches can update their profile information effectively.
- **Link to Video**: [Coach Profile Management](https://drive.google.com/file/d/1nZJO9wsUx_ISMgdaiyylSs28uQ2jiX8a/view?usp=sharing)

### 🛠️ Administrative Functions
- **Description**: Administrative tools and features for managing the platform.
##### 🎥 Admin Login and Adding a Coach
- **Description**: This tutorial covers the administrative functions of logging in and adding a new coach.
- **Link to Video**: [Admin Login and Adding a Coach](https://drive.google.com/file/d/1hDNXGYA8OKeqjJcpK1TxZUvsaoTzEe6K/view?usp=sharing)



