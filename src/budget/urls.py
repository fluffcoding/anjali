from django.urls import path

from .views import expenseApprovalRequest, indexRedirect, expenseApprovalView, allExpensesView, index, settingsView, profileEdit

urlpatterns = [
    path('', index, name='iredirect'),
    path('expense', expenseApprovalRequest, name='expenseApprovalRequest'),
    path('approve-expenses/<id>', expenseApprovalView, name='expenseApprovalView'),
    path('all-expenses/<id>', allExpensesView, name='allExpensesView'),
    path('settings', settingsView, name='settings'),
    path('profile-edit/<id>', profileEdit, name='editProfile')
]
