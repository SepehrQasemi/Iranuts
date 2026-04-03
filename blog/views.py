from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from config.mixins import AdminRequiredMixin

from .forms import PostForm
from .models import Post


class PostView(ListView):
    model = Post 
    template_name = 'blog/post_list.html'
    context_object_name = 'post_list'

class PostDetails(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostEdit(AdminRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
    context_object_name = 'post'

class PostDelete(AdminRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('Blog')

class PostCreate(AdminRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
