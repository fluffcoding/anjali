from django.contrib import admin

# Register your models here.
from .models import Department, Expenses, Profile


admin.site.register(Department)
# admin.site.register(Budget)
admin.site.register(Expenses)
admin.site.register(Profile)