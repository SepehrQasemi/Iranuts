from django.views.generic import CreateView,TemplateView,DetailView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import CustomUser
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib import messages

class LogedInView(TemplateView):
    template_name = 'registration/logedin.html'

class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if form.errors.get('phone_no',None):
            if 'exists' in str(form.errors['phone_no']):
                messages.error(self.request, 'This phone number already used')
            else:
                messages.error(self.request,'Wrong format for phone number')

        if form.errors.get('password',None):

            if 'match' in str(form.errors['password2']):
                messages.error(self.request,'Passwords do not match')

            else:
                messages.error(self.request,'Password is too simple')


        return response



class ProfileView(LoginRequiredMixin,DetailView):
    model = CustomUser
    template_name = 'profile.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if not request.user==self.get_object():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    

class ProfileEdit(UserPassesTestMixin,UpdateView):
    model=CustomUser
    template_name='ProfileEdit.html'
    fields =['first_name', 'last_name','address']

    def get_success_url(self):
        return reverse_lazy ('Profile',args = (self.object.id,))
    
    def test_func(self):
        return  self.request.user==self.get_object()
    