from django.shortcuts import render, redirect
from django.contrib import messages

from emails.models import Email, EmailVerificationEvent
from emails.forms import EmailForm
from emails import services

# Create your views here.

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
    if not verified:
        try:
            del request.session['email_id']
        except:
            pass
        messages.error(request, msg)
        return redirect("/login/")
    
    messages.success(request, msg)
    request.session['email_id'] = f"{email_obj.id}"
    next_url = request.session.get('next_url') or "/"
    if not next_url.startswith("/"):
        next_url = "/"
    return redirect(next_url)