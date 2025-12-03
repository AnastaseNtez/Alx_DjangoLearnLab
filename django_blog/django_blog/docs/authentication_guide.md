Django Blog Authentication System Guide

This document details the user authentication system implemented in the django_blog project, covering user flows for registration, login, logout, and profile management.

1. Overview

The system utilizes Django's built-in authentication framework for robust security (password hashing, session management) and extends it with custom views and forms for enhanced user experience.

Feature

URL Pattern

Implementation

Registration

/register/

Custom view (blog/views.py) using a custom form (blog/forms.py) to include the user's email.

Login

/login/

Built-in Django LoginView (uses blog/login.html template).

Logout

/logout/

Built-in Django LogoutView (uses blog/logout.html template).

Profile

/profile/

Custom view (blog/views.py) protected by the @login_required decorator.

2. Code Components

blog/forms.py

Form: CustomUserCreationForm

Function: Inherits from UserCreationForm but explicitly includes the email field in the Meta class and ensures it is required in the __init__ method.

blog/views.py

register(request): Handles form submission and saving of new users. Uses Django's messages framework to provide success feedback and redirects to the login page upon successful account creation.

profile(request): Displays the current user's details (username, email). It is secured using the @login_required decorator, meaning unauthenticated users are automatically redirected to the login page.

django_blog/urls.py

Includes the built-in LoginView and LogoutView from django.contrib.auth.views and points them to the correct custom templates (blog/login.html, blog/logout.html).

3. Testing Instructions

To test the system, ensure your Django development server is running.

3.1. Test Registration

Navigate to the registration page: http://127.0.0.1:8000/register/

Fill in a desired username, email address, and a secure password (twice).

Click "Sign Up".

Expected Result: You should see a success message (Account created for X! You can now log in.) and be redirected to the login page.

3.2. Test Login

Navigate to the login page: http://127.0.0.1:8000/login/

Enter the credentials for the user you just created.

Click "Login".

Expected Result: You should be redirected to the home page (/) and see the welcome message: "Hello, [Username]! You are logged in..."

3.3. Test Profile Access

While logged in, click the "Profile" link in the header or navigate to: http://127.0.0.1:8000/profile/

Expected Result: The profile page should load, displaying your username and email.

3.4. Test Logout

While logged in, click the "Logout" link in the header or navigate to: http://127.0.0.1:8000/logout/

Expected Result: You should be redirected to the logout confirmation page, then automatically to the home page, where the header links change back to "Login" and "Register".