from django.contrib import admin
from .models import Student, Project, ProjectSkills,UserProfile,ApplyProject


admin.site.register(Student)
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectSkills)
admin.site.register(ApplyProject)

