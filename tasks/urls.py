from django.urls import path
from tasks import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name="tasks-list"),
    path('<int:pk>/', views.TaskDetailView.as_view(), name="task-detail"),
    path('<int:pk>/update', views.TaskUpdateView.as_view(), name="task-update"),
    path('<int:pk>/delete', views.TaskDeleteView.as_view(), name="task-delete"),
    path('task-create/', views.TaskCreationView.as_view(), name="task-create"),
    path("<int:pk>/complete/", views.TaskCompleteView.as_view(), name="task-complete"),
    path("comment/update/<int:pk>", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comment/delete/<int:pk>", views.CommentDeleteView.as_view(), name="comment-delete"),
    path("comment/like/<int:pk>", views.CommentLikeToggle.as_view(), name="comment-like-toggle"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),

]

app_name = "tasks"