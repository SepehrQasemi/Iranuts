from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["phone"].help_text = "Use the same phone number when signing in."
        self.fields["phone"].widget.attrs.update(
            {"placeholder": "09123456789", "autocomplete": "tel"}
        )
        self.fields["email"].widget.attrs.update({"autocomplete": "email"})

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user


class PhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Phone number", max_length=13)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "09123456789",
                "autocomplete": "tel",
            }
        )
        self.fields["password"].widget.attrs.update({"autocomplete": "current-password"})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "address"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
