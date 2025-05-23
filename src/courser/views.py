from django.shortcuts import render

# Note: template paths here are relative to the path in 
# 'DIRS' in 'TEMPLATES' in 'settings.py'

def home(request):
    return render(request, "home.html", {})