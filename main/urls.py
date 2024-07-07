from django.urls import path
from .views import HomeView, DirectionView, TaskView, LoginRegisterView, LoginView, RegisterView, TaskDetailView

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('direction/<int:id>/', DirectionView.as_view(), name="direction"),
    # path('subject/tasks/<int:science_id>/', SubjectView.as_view(), name='subject'),
    path('subject/tasks/<int:subject_id>/', TaskView.as_view(), name='task'),
    path('task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),

    # path('subject/<str:slug>/task/<int:id>', SubjectTaskView.as_view(), name="subject_task"),
    path('login-register/', LoginRegisterView.as_view(), name='login-register'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register')
]
