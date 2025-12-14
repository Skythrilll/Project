# Email Configuration Guide for Contact Form

## Current Setup
The contact form is now functional and will send emails to: c18adarsh@gmail.com

## For Development (Current Configuration)
Currently using console backend - emails will be printed to the terminal/console where the Django server is running.
This is useful for testing without sending real emails.

## To Enable Real Email Sending with Gmail

### Step 1: Enable 2-Step Verification in Gmail
1. Go to your Google Account: https://myaccount.google.com/
2. Click on "Security" in the left sidebar
3. Enable "2-Step Verification" if not already enabled

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Sign in to your Gmail account (c18adarsh@gmail.com)
3. Select app: "Mail"
4. Select device: "Other (Custom name)" and enter "Django Grocery App"
5. Click "Generate"
6. Copy the 16-character app password (it will look like: xxxx xxxx xxxx xxxx)

### Step 3: Update settings.py
Open `gp/settings.py` and make these changes:

1. Comment out the console backend line:
   ```python
   # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
   ```

2. Uncomment and configure the SMTP settings:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'c18adarsh@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-16-char-app-password-here'  # Paste the app password from Step 2
   DEFAULT_FROM_EMAIL = 'c18adarsh@gmail.com'
   ```

### Step 4: Test the Contact Form
1. Restart your Django server
2. Go to the contact page
3. Fill out the form and submit
4. You should receive an email at c18adarsh@gmail.com

## Security Notes
- NEVER commit your app password to version control (Git)
- Consider using environment variables for sensitive data:
  ```python
  import os
  EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
  ```
- The app password is different from your regular Gmail password
- If you suspect the app password is compromised, revoke it and generate a new one

## Troubleshooting
- If emails don't arrive, check your spam folder
- Make sure 2-Step Verification is enabled in Google Account
- Verify the app password is correct (no spaces)
- Check the Django console for any error messages
- Gmail has sending limits (500 emails per day for free accounts)

## Alternative: Using Console Backend for Testing
If you want to test without setting up Gmail:
- Keep the current console backend configuration
- Emails will be printed in the terminal where you run `python manage.py runserver`
- This is useful for development and testing
