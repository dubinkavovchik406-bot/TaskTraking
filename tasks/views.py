from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from tasks import models
from tasks.mixins import UserIsOwnerMixin
from tasks.forms import TaskForm, TaskFilterForm, CommentForm

from django.db.models import F
from datetime import timedelta
from django.utils import timezone

# Сторінка з усіма тасками
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task-list.html"

    # Отримання queryset з запиту для застосування фільтра
    def get_queryset(self):
        # Початковий QuerySet
        queryset = super().get_queryset().order_by(
            F('due_date').asc(nulls_last=True),'-priority'
        )

        # Обробка Фільтрації
        form = TaskFilterForm(self.request.GET)

        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Фільтри за Статусом
            status_filter = cleaned_data.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            # Фільтри за Пріоритетом
            priority_filter = cleaned_data.get('priority')
            if priority_filter:
                queryset = queryset.filter(priority=priority_filter)

            # Фільтрація за Датою
            due_date_period = cleaned_data.get('due_date_period')

            if due_date_period:
                today = timezone.localdate()

                if due_date_period == 'today':
                    # Фільтр - Час сьогодні
                    queryset = queryset.filter(due_date=today)
                elif due_date_period == 'this_week':
                    # Фільтр - Час цього тижня
                    days_until_sunday = 6 - today.weekday()
                    end_of_week = today + timedelta(days=days_until_sunday)
                    queryset = queryset.filter(due_date__lte=end_of_week, due_date__gte=today)
                elif due_date_period == 'overdue':
                    # Фільтр - прострочены задачі і статус не done
                    queryset = queryset.filter(due_date__lt=today, status__in=['todo', 'in_progress'])
                    return queryset

        return queryset

    # Збереження параметрів фільтру у контекст для використання у шаблоні
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context

# Сторінка з деталями таска
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task-detail.html"

    # Збереження параметрів фільтру у контекст для використання у шаблоні
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    # Для обробки post запиту на створення комменту й медиа файлу(у наступному ще й лайку)
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk=comment.task.pk)
        else:
            pass

# Сторінка для створення таску
class TaskCreationView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = "tasks/task-form.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:tasks-list")

    # Чи валідна форма таску
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

# Сторінка для зміни статусу таску на done одним нажатием
class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("tasks:tasks-list"))

    # Отримання поточного таску
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)

# Сторінка для зміни інформації про таску
class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    form_class = TaskForm
    template_name = "tasks/task-update-form.html"
    success_url = reverse_lazy("tasks:tasks-list")

# Сторінка для видалення таску
class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy("tasks:tasks-list")
    template_name = "tasks/task-delete-confirmation.html"

