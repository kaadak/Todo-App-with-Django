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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from django.contrib.auth.views import LoginView
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            queryset = queryset.filter(title__startswith=search_input)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['count'] = context['tasks'].filter(complete=False).count()
        context['search_input'] = self.request.GET.get('search-area') or ''

        return context

@method_decorator(never_cache, name='dispatch')
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

@method_decorator(never_cache, name='dispatch')
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

@method_decorator(never_cache, name='dispatch')
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object = 'task'
    template_name = 'core/task_confirm_delete.html'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True


class RegisterPage(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('tasks')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('tasks')  

    