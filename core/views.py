from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Task
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls  import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object = 'task'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object = 'task'
    template_name = 'core/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)



class RegisterPage(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('tasks')  

    