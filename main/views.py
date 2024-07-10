from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from .models import User, Welcome, AboutPlatform, Directions, Sciences, Subject, Problems, Contact, Variant, Question, \
    Category, Result, QuestionResult
from django.contrib import messages
from django.utils import timezone
import json
from django.http import HttpResponseBadRequest


class HomeView(View):
    def get(self, request, *args, **kwargs):
        welcome = Welcome.objects.all()
        about_platform = AboutPlatform.objects.all()
        direction = Directions.objects.all()
        context = {'welcome': welcome, 'about_platforms': about_platform, 'directions': direction}
        return render(request, 'index.html', context=context, status=200)

    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        Contact.objects.create(name=name, phone=phone, email=email)
        messages.success(request, 'Muvaffaqiyattli Ro\'yxatdan olindi')
        return redirect('main:home')


class DirectionView(View):
    def get(self, request, *args, **kwargs):
        direction = get_object_or_404(Directions, id=self.kwargs['id'])
        sciences = Sciences.objects.filter(directions=direction)
        directions = Directions.objects.all()
        context = {'direction': direction, 'sciences': sciences, 'directions': directions}
        return render(request, 'direction.html', context=context, status=200)


class TaskView(View):
    def get(self, request, *args, **kwargs):
        subject_id = self.kwargs['subject_id']
        subject = get_object_or_404(Subject, id=subject_id)
        tasks = Problems.objects.filter(subject=subject)
        directions = Directions.objects.all()
        return render(request, 'task.html', context={'subject': subject, 'tasks': tasks,
                                                     'directions': directions})


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Problems, id=task_id)
        directions = Directions.objects.all()
        categories = Category.objects.filter(subject=task.subject)
        context = {'task': task, 'directions': directions, 'categories': categories}
        return render(request, 'task_detail.html', context=context)


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


class QuizView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        questions = Question.objects.filter(category=category).prefetch_related('variants')
        questions_with_correct_variant = []
        
        for question in questions:
            variants = question.variants.all()
            correct_variant_id = None
            for variant in variants:
                if variant.is_true:
                    correct_variant_id = variant.id
                    break
            questions_with_correct_variant.append((question, variants, correct_variant_id))
        
        return render(request, 'test.html', {'category': category, 'questions_with_correct_variant': questions_with_correct_variant})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        questions = Question.objects.filter(category=category)        
        result = {
            'category_id': category.id,  # Add category_id to the result object
            'score': 0,
            'fail': 0,
            'question_results': []
        }
        for question in questions:
            selected_variant_id = request.POST.get(f'question_{question.id}')
            if selected_variant_id:
                selected_variant = get_object_or_404(Variant, id=selected_variant_id)
                correct_variant = question.variants.get(is_true=True)
                is_correct = selected_variant == correct_variant

                result['question_results'].append({
                    'question_id': question.id,
                    'correct_variant_id': correct_variant.id,
                    'selected_variant_id': selected_variant.id,
                    'is_correct': is_correct
                })

                if is_correct:
                    result['score'] += 1
                else:
                    result['fail'] += 1

        response = redirect('main:result')
        response.set_cookie('quiz_result', json.dumps(result), max_age=604800 * 2)
        return response

    

class ResultView(View):
    def get(self, request):
        quiz_result_str = request.COOKIES.get('quiz_result')
        if not quiz_result_str:
            return HttpResponseBadRequest("Quiz result cookie not found.")
        
        try:
            result = json.loads(quiz_result_str)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid quiz result data.")

        return render(request, 'test_result.html', {'result': result})