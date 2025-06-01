from django.shortcuts import render, redirect
from django.contrib import messages

from emails.forms import EmailForm
from emails import services

from django_htmx.http import HttpResponseClientRedirect

# Create your views here.

import config

def logout_btn_view(request):
    if not request.htmx:
        return redirect('/')
    
    if request.method == "POST":
        try:
            del request.session['email_id']
        except:
            pass
        email_id_session = request.session.get('email_id')
        if not email_id_session:
            return HttpResponseClientRedirect('/')
    return render(request, "emails/logout_btn.html", {})

def email_token_login_view(request):
        
    if not request.htmx:
        return redirect('/')

    template = "emails/email_form.html"
    # This will be invaid if the argument is none
    email_input = EmailForm(request.POST or None)
    email_id_session = request.session.get('email_id')
    context = {
        "email_input": email_input,
        "message": "",
        "user_logged_in": email_id_session
    }
    if email_input.is_valid():
        # cleaned_data returns a dictionary without html tags
        email_input = email_input.cleaned_data.get('email')
        _ = services.create_email_verification(email_input)

        context['form'] = EmailForm()
        context['message'] = (
            "Succcess! Check your email for verification from "+
            f"{config.get_email_env("EMAIL_HOST_USER")}"
        )
    else:
        print(email_input.errors)
    
    return render(request, template, context)

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