from django import forms

from .models import Expenses, Department, Profile

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', )


class DateInput(forms.DateInput):
    input_type = 'date'


class expenseApprovalForm(forms.ModelForm):
    hotel_rent = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    transport = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    meal = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    # travel_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Travel Date'}))
    airfare = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    others = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Amount in PKR'}))
    remarks = forms.Textarea()
    class Meta:
        model = Expenses
        exclude = ['employee','form_status_head','form_status_payment','total_amount', 'department']
        widgets = {
            'travel_date': DateInput(),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)