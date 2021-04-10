from django.db import models

# from django.contrib.auth.models import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
# from django.utils import timezone

from django.contrib.auth import get_user_model

from django.utils.timezone import now


User = get_user_model()

# from .base import UserManager

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    budget_monthly = models.IntegerField(default=50000)


    def remaining_monthly_budget(self):
        expenses = Expenses.objects.filter(department=self, form_status_head=True, form_status_payment=True)
        total = 0
        for expense in expenses:
            total += expense.total_amount
        return self.budget_monthly - total


    def expense_approval(self, id):
        exp = Expenses.objects.get(id=id)
        if self.remaining_monthly_budget() < exp.total_amount:
            return False
        else:
            return True
    

    def __str__(self):
        return self.department_name



# class User(AbstractBaseUser, PermissionsMixin):
#     first_name = models.CharField(max_length=100,default="dufault")
#     last_name = models.CharField(max_length=100,default="dufault")
#     username = models.CharField(max_length=100)
#     user_number = models.IntegerField(null=True, blank=True)
#     email = models.EmailField(unique=True)
#     user_salary = models.IntegerField(null=True, blank=True)
#     user_role = models.CharField(max_length=100, null=True, blank=True)
#     department = models.ForeignKey(Department, models.CASCADE, default='2')
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(default=timezone.now)
#     head = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def get_full_name(self):
#         '''
#         Returns the first_name plus the last_name, with a space in between.
#         '''
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def get_short_name(self):
#         '''
#         Returns the short name for the user.
#         '''
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         '''
#         Sends an email to this User.
#         '''
#         send_mail(subject, message, from_email, [self.email], **kwargs)
    

#     def create_user(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(username, email, password, **extra_fields)

#     def create_superuser(self, username, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self._create_user(username, email, password, **extra_fields)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default='2', null=True, blank=True) 
    # department default=2 (uncategorized)
    head = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)



class Expenses(models.Model):
    employee = models.ForeignKey(User,models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    travel_date = models.DateField(default=now)
    airfare = models.IntegerField(null=True, blank=True)
    hotel_rent = models.IntegerField(null=True, blank=True)
    transport = models.IntegerField(null=True, blank=True)
    meal = models.IntegerField(null=True, blank=True)
    others = models.IntegerField(default=0)
    remarks = models.TextField(null=True, blank=True)
    form_status_head = models.BooleanField(default=None, null=True, blank=True)
    form_status_payment = models.BooleanField(default=None, null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)


    def total(self):
        total = self.airfare + self.hotel_rent + self.transport + self.meal + self.others
        self.total_amount = total
        return total


    def form_status(self):
        if self.form_status_head is True and self.form_status_payment is True:
            return True
        elif self.form_status_head is False or self.form_status_payment is False:
            return False
        elif self.form_status_head is None or self.form_status_payment is None:
            return None
        else:
            return False

# class Budget(models.Model):
#     department = models.ForeignKey(Department,models.CASCADE)
#     budget_monthly = models.IntegerField(default=50000)
#     # budget_yearly = models.IntegerField(default=600000)


#     def remaining_monthly_budget(self):
#         expenses = Expenses.objects.filter(department=self.department, form_status=True)
#         total = 0
#         for expense in expenses:
#             total += expense.total_amount
#         return self.budget_monthly - total


#     # def remaining_yearly_budget(self):
#     #     expenses = Expenses.objects.filter(department=self.department, form_status=True)
#     #     total = 0
#     #     for expense in expenses:
#     #         total += expense.total_amount
#     #     return self.budget_yearly - total


    
#     def expense_approval(self, id):
#         exp = Expenses.objects.get(id=id)
#         if self.remaining_monthly_budget() < exp.total_amount:
#             return False
#         else:
#             return True


class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE)
    