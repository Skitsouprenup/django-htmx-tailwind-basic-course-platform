from django.shortcuts import render

from emails import services

from emails.forms import EmailForm

import config

# Note: template paths here are relative to the path in 
# 'DIRS' in 'TEMPLATES' in 'settings.py'

# Note: This is for debugging only. Use the 'email_token_login_view'
# view in 'emails' app.
def home(request):
    # This will be invaid if the argument is none
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        # cleaned_data returns a dictionary without html tags
        email_input = form.cleaned_data.get('email')
        obj = services.create_email_verification(email_input)

        context['email_input'] = EmailForm()
        context['message'] = (
            "Succcess! Check your email for verification from "+
            f"{config.get_email_env("EMAIL_HOST_USER")}"
        )
    else:
        print(form.errors) 
    
    return render(request, "home.html", context)