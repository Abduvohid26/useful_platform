from django.contrib import admin
from .models import User, Welcome, AboutPlatform, Directions, Sciences, Subject ,\
    Problems, ProblemImages

admin.site.register([User, Welcome, AboutPlatform, Directions, 
                     Sciences, Subject, Problems, ProblemImages])
