from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView,DeleteView,UpdateView,CreateView
from django.urls import reverse_lazy


class PostView(ListView):
    model = Post 
    template_name = 'Blog.html'
    context_object_name = 'post_list'

class PostDetails(DetailView):
    model = Post
    template_name = 'PostDetails.html'
    context_object_name = 'Post'

class PostEdit(UpdateView):
    model = Post
    template_name = 'PostEdit.html'
    fields=['title','summaries','body',]
    def test_func(self):
        return self.request.user.is_superuser

class PostDelete(DeleteView):
    model = Post
    template_name = 'PostDelete.html'
    context_object_name = 'Post'
    fields = '__all__'
    success_url = reverse_lazy('Blog')
    def test_func(self):
        return self.request.user.is_superuser

class PostCreate(CreateView):
    model = Post
    template_name = 'PostCreate.html'
    fields = '__all__'
    def test_func(self):
        return self.request.user.is_superuser