from django.contrib import admin
from .models import (User, Welcome, AboutPlatform, Directions, Sciences, Subject, Problems, ProblemImages, Contact,
                     Question, Category, Variant, Result, MainPage)

admin.site.register([User, Welcome, AboutPlatform, Directions, Sciences, Subject, Problems, ProblemImages, Contact,
                     Variant, Result, MainPage])


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'quiz_count']
    readonly_fields = ['quiz_count']


class VariantInline(admin.TabularInline):
    model = Variant


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['category', 'title']
    inlines = [VariantInline]
