from django.contrib import admin
from .models import Student, Project, ProjectSkills


admin.site.register(Student)

admin.site.register(Project)
admin.site.register(ProjectSkills)

