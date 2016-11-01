from django.contrib import admin
from .models import Student, Project, ProjectSkills


admin.site.register(Student) # Register a student

admin.site.register(Project) # Register a project
admin.site.register(ProjectSkills) # Register project skills

