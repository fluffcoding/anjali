from django.urls import path

from .views import expenseApprovalRequest, indexRedirect, expenseApprovalView, allExpensesView, index, settingsView, profileEdit, profileCreate, paymentsView, singlePayment

urlpatterns = [
    path('', index, name='iredirect'),
    path('expense', expenseApprovalRequest, name='expenseApprovalRequest'),
    path('approve-expenses/<id>', expenseApprovalView, name='expenseApprovalView'),
    path('all-expenses/<id>', allExpensesView, name='allExpensesView'),
    path('settings', settingsView, name='settings'),
    path('profile-edit/<id>', profileEdit, name='editProfile'),
    path('profile-create', profileCreate, name='profileCreate'),
    path('payments', paymentsView, name='payments'),
    path('payment/<id>', singlePayment, name='single-payments'),
]
