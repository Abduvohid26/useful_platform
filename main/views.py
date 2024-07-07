from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from .models import User, Welcome, AboutPlatform, Directions, Sciences, Subject, Problems
from django.contrib import messages

# Create your views here.


class HomeView(View):
    def get(self, request, *args, **kwargs):
        welcome = Welcome.objects.all()
        about_platform = AboutPlatform.objects.all()
        direction = Directions.objects.all()
        context = {'welcome': welcome, 'about_platforms': about_platform, 'directions': direction}
        return render(request, 'index.html', context=context, status=200)


class DirectionView(View):
    def get(self, request, *args, **kwargs):
        direction = get_object_or_404(Directions, id=self.kwargs['id'])
        sciences = Sciences.objects.filter(directions=direction)
        context = {'direction': direction, 'sciences': sciences}
        return render(request, 'direction.html', context=context, status=200)


# class SubjectView(View):
#     def get(self, request, *args, **kwargs):
#         science_id = self.kwargs['science_id']
#         science = get_object_or_404(Sciences, id=science_id)
#         subjects = Subject.objects.filter(sciences=science)
#         return render(request, 'task.html', context={'science': science, 'subjects': subjects})


class TaskView(View):
    def get(self, request, *args, **kwargs):
        subject_id = self.kwargs['subject_id']
        subject = get_object_or_404(Subject, id=subject_id)
        tasks = Problems.objects.filter(subject=subject)
        return render(request, 'task.html', context={'subject': subject, 'tasks': tasks})


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Problems, id=task_id)
        print(task.name)
        return render(request, 'task_detail.html', context={'task': task})


class LoginRegisterView(View):
    def get(self, request):
        return render(request, 'login-register.html')


class LoginView(View):
    def post(self, request):
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                messages.warning(request, 'User not found')
                return redirect('main:login-register')
        else:
            username = username_or_email
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('main:login-register')
        else:
            messages.warning(request, 'Invalid username-email or password')
            return redirect('main:login-register')


class RegisterView(View):
    def post(self, request):
        complete_name = request.POST.get('signupname')
        email = request.POST.get('signupemail')
        password = request.POST.get('signupphone')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('main:login-register')

        if User.objects.filter(username=complete_name).exists():
            messages.warning(request, 'Username already exists')
            return redirect('main:login-register')

        User.objects.create_user(username=complete_name, email=email, password=password)
        messages.success(request, 'User created successfully. You can now log in')
        return redirect('main:login-register')


