from django.shortcuts import render

# Create your views here.
from emails.models import Email, EmailVerificationEvent
from emails.forms import EmailForm
from emails import services

import config

def home_view(request):
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

        context['form'] = EmailForm()
        context['message'] = (
            "Succcess! Check your email for verification from "+
            f"{config.get_email_env("")}"
        )
    else:
        print(form.errors) 
    
    return render(request, "home.html", context)

def verify_email_token_view(request, token):
    verified, msg, email_obj = services.verify_token(token)