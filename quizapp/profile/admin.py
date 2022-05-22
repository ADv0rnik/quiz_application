from django.contrib import admin

from profile.models import Student, Results, TechStack


class TechStackInLine(admin.TabularInline):
    model = TechStack


class StudentAdmin(admin.ModelAdmin):
    inlines = [TechStackInLine]


admin.site.register(Student, StudentAdmin)
admin.site.register(Results)
admin.site.register(TechStack)
