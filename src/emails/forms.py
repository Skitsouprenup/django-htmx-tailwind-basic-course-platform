from django import forms
from .models import Email

from emails import services

class EmailForm(forms.Form):
    __EMAIL_FIELD_CSS = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"

    email = forms.EmailField(
        #input type
        widget=forms.EmailInput(
            #html attributes
            attrs={
                "id":"email-login",
                "class":__EMAIL_FIELD_CSS,
                "placeholder":"E-mail Address"
            }
        )
    )

    # This is called when forms.EmailInput.isvalid() method is called.
    def clean_email(self):
        # cleaned_data returns a dictionary without html tags
        email_input = self.cleaned_data.get("email")
        
        if services.email_not_active(email_input):
            raise forms.ValidationError("Email is not activated.")
        return email_input