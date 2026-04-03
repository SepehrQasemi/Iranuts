from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from config.mixins import UserOwnsObjectOrAdminMixin

from .forms import ProfileForm, SignUpForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/registration/signup.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if form.errors.get('phone',None):
            if 'exists' in str(form.errors['phone']):
                messages.error(self.request, 'This phone number already used')
            else:
                messages.error(self.request,'Wrong format for phone number')

        if form.errors.get('password2',None):
            if 'match' in str(form.errors['password2']):
                messages.error(self.request,'Passwords do not match')
            else:
                messages.error(self.request,'Password is too simple')

        return response


class ProfileView(UserOwnsObjectOrAdminMixin,DetailView):
    model = CustomUser
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'

class ProfileEdit(UserOwnsObjectOrAdminMixin,UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'
    context_object_name = 'profile_user'

    def get_success_url(self):
        return reverse_lazy('accounts:profile', args=(self.object.id,))
