from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from .models import User, Welcome, AboutPlatform, Directions, Sciences, Subject, Problems, Contact, Variant, Question, \
    Category, MainPage, Result, QuestionResult
from django.contrib import messages
from .forms import SubjectSelectForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SubjectSelectForm(data=request.GET)
        welcome = Welcome.objects.all()
        about_platform = AboutPlatform.objects.all()
        direction = Directions.objects.all()
        main_page = MainPage.objects.all()
        subject = Subject.objects.all()
        question = Question.objects.all()
        subject_count = subject.count()
        if form.is_valid():
            subject = form.cleaned_data['subject']
            category = Category.objects.filter(subject=subject).first()
            if category:
                return redirect('main:quiz', category_id=category.id)
        
        context = {
            'welcome': welcome,
            'about_platforms': about_platform,
            'directions': direction,
            'main_pages': main_page,
            'form': form,
            'subject_count': subject_count,
            'questions': question
        }
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
        main_page = MainPage.objects.all()
        context = {'direction': direction, 'sciences': sciences, 'directions': directions, 'main_pages': main_page}
        return render(request, 'direction.html', context=context, status=200)


class TaskView(View):
    def get(self, request, *args, **kwargs):
        subject_id = self.kwargs['subject_id']
        subject = get_object_or_404(Subject, id=subject_id)
        tasks = Problems.objects.filter(subject=subject)
        directions = Directions.objects.all()
        main_page = MainPage.objects.all()
        return render(request, 'task.html', context={'subject': subject, 'tasks': tasks,
                                                     'directions': directions, 'main_pages': main_page})


class TaskDetailView(View):
    def get(self, request, *args, **kwargs):
        task_id = self.kwargs['task_id']
        task = get_object_or_404(Problems, id=task_id)
        directions = Directions.objects.all()
        categories = Category.objects.filter(subject=task.subject)
        main_page = MainPage.objects.all()
        context = {'task': task, 'directions': directions, 'categories': categories, 'main_pages': main_page}
        return render(request, 'task_detail.html', context=context)


class LoginRegisterView(View):
    def get(self, request):
        directions = Directions.objects.all()
        main_page = MainPage.objects.all()
        return render(request, 'login-register.html', context={'directions': directions, 'main_pages': main_page})


class LoginView(View):
    def post(self, request):
        username_or_email = request.POST.get('email')
        password = request.POST.get('password')
        if '@' in username_or_email:
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                messages.warning(request, f'Bunday user topilmadi')
                return redirect('main:login-register')
        else:
            username = username_or_email
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyattli kirdingiz')
            return redirect('main:home')
        else:
            messages.warning(request, 'ism yoki email manzil xato kiritildi')
            return redirect('main:login-register')


class RegisterView(View):
    def post(self, request):
        complete_name = request.POST.get('signupname')
        email = request.POST.get('signupemail')
        password = request.POST.get('signupphone')

        if User.objects.filter(email=email).exists():
            messages.warning(request, 'mavjud email manzil kiritildi !')
            return redirect('main:login-register')

        if User.objects.filter(username=complete_name).exists():
            messages.warning(request, 'mavjud ism kiritildi !')
            return redirect('main:login-register')

        User.objects.create_user(username=complete_name, email=email, password=password)
        messages.success(request, 'Muvaffaqiyattli ro\'yxatdan o\'tdingiz ')
        return redirect('main:login-register')


class QuizView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        questions = Question.objects.filter(category=category).prefetch_related('variants')
        directions = Directions.objects.all()
        main_page = MainPage.objects.all()
        return render(request, 'test.html', {'category': category, 'questions': questions, 
                                             'directions': directions, 'main_pages': main_page})

    def post(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        questions = Question.objects.filter(category=category)
        result = Result.objects.create(category=category, score=0, success=0, fail=0)

        for question in questions:
            selected_variant_id = request.POST.get(f'question_{question.id}')
            if selected_variant_id:
                selected_variant = get_object_or_404(Variant, id=selected_variant_id)
                correct_variant = question.variants.get(is_true=True)
                is_correct = selected_variant == correct_variant

                QuestionResult.objects.create(
                    result=result,
                    question=question,
                    correct_variant=correct_variant,
                    selected_variant=selected_variant,
                    is_correct=is_correct
                )

                if is_correct:
                    result.score += 1
                    result.success += 1
                else:
                    result.fail += 1

        result.save()
        return redirect('main:result', result_id=result.id)


class ResultView(View):
    def get(self, request, result_id):
        directions = Directions.objects.all()
        main_page = MainPage.objects.all()
        result = get_object_or_404(Result, id=result_id)
        return render(request, 'test_result.html', {'result': result, 'directions': directions, 
                                                'main_pages': main_page})