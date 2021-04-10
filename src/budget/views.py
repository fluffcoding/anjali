from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from .forms import expenseApprovalForm, DepartmentForm, UserForm, ProfileForm, NewDepartmentForm

from .models import Expenses, Department, Profile, Payment

from django.contrib.auth.models import User


@login_required
def indexRedirect(request):
    profile = Profile.objects.get(user=request.user)

    if request.user.is_authenticated:
        if profile.head:
            return redirect('expenseApprovalView', profile.department.id)
        else:
            return redirect('expenseApprovalRequest')
    else:
        return redirect('expenseApprovalRequest')


@login_required
def expenseApprovalRequest(request):
    employeesExpenses = Expenses.objects.filter(employee=request.user).order_by('-id')
    form = expenseApprovalForm(request.POST or None)
    profile = Profile.objects.get(user=request.user)
    department = profile.department
    if form.is_valid():
        expense = form.save(commit=False)
        expense.employee = request.user
        total = int(form.cleaned_data['airfare']) + int(form.cleaned_data['hotel_rent']) + int(form.cleaned_data['transport']) + int(
            form.cleaned_data['meal']) + int(form.cleaned_data['others'])
        expense.total_amount = total
        expense.department = profile.department
        expense.save()
        if department.expense_approval(expense.id):
            pass
        else:
            expense.form_status_head = False
            expense.save()
        return redirect('expenseApprovalRequest')
    context = {
        'form': form,
        'expenses': employeesExpenses,
        'department': department
    }
    return render(request, 'expense_approval/form.html', context)



@login_required
def expenseApprovalView(request, id):
    department = Department.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    if profile.head and profile.department == department:
        department = profile.department
        expenses = Expenses.objects.filter(form_status_head=None, department=department)
        if request.method == 'POST':
            print(request.POST)
            expense = Expenses.objects.get(id=int(request.POST.get('id')))
            status = request.POST.get('switch')
            if status == 'on':
                expense.form_status_head = True
                expense.save()
            else:
                expense.form_status_head = False
                expense.save()
            return redirect('expenseApprovalView', profile.department.id)
        context = {
            'expenses': expenses,
            'department': department,
            # 'budget': budget,
        }
        return render(request, 'expense_requests/head.html', context)
    else:
        return HttpResponse('<h1>You need to be a department head to access this view. <a href="/expense">Go to expense page</a></h1>')


@login_required
def allExpensesView(request, id):
    department = Department.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    if profile.head and profile.department == department:
        expenses = Expenses.objects.filter(department=department)
        context = {
            'expenses': expenses,
            'department': department,
        }
        return render(request, 'expense_requests/all.html', context)
    else:
        return HttpResponse("<h1>You need to be this department's head to access this view. <a href='/expense'>Go to expense page</a></h1>")


def index(request):
    user = request.user
    context = {'user': user}
    return render(request, 'index.html', context)


def settingsView(request):
    form = NewDepartmentForm(request.POST or None)
    depts = Department.objects.all()
    user_form = UserForm(request.POST or None)
    users = User.objects.filter(is_staff=False)
    if form.is_valid():
        form.save()
        return redirect('settings')
    elif user_form.is_valid():
        user = User.objects.create_user(**user_form.cleaned_data)
        user.save()
        print('user saved')
        return redirect('settings')
    context = {
        'form': form,
        'depts': depts,
        'user_form': user_form,
        'users': users,
    }
    return render(request, 'settings/main.html', context)


def profileEdit(request, id):
    if request.user.profile.admin:
        user = User.objects.get(id=id)
        profile = Profile.objects.get(user=user)
        form = ProfileForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('editProfile', user.id)
        context = {
            'form': form,
            'user': user,
        }
        return render(request, 'profile/edit.html', context)
    else:
        return HttpResponse("<h1>Not Authorized</h1>")


@login_required
def profileCreate(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = DepartmentForm(request.POST or None)
    if form.is_valid():
        profile.department = form.cleaned_data['department']
        profile.save()
        print(form.cleaned_data)
        return redirect('iredirect')
    context = {
        'form': form,
    }
    return render(request, 'profile/create.html', context)

@login_required
def paymentsView(request):
    if request.user.profile.admin:
        expenses = Expenses.objects.all()
        if request.method == "POST":
            if 'approve' in request.POST:
                id = request.POST.get('id')
                the_expense = Expenses.objects.get(id=id)
                the_expense.form_status_payment = True
                the_expense.save()
                return redirect('payments')
            if 'reject' in request.POST:
                id = request.POST.get('id')
                the_expense = Expenses.objects.get(id=id)
                the_expense.form_status_payment = False
                the_expense.save()
                return redirect('payments')
        context = {
            'expenses': expenses
        }
        return render(request, 'payment/main.html', context)
    else:
        return HttpResponse('<h1>You are not registered as an admin.<a href="/">Go Home</a></h1>')


def singlePayment(request, id):
    expense = Expenses.objects.get(id=id)
    try:
        payment_status = Payment.objects.get(expense=expense)
    except:
        payment_status = False
    print(payment_status)

    if request.method == 'POST':
        # id = int(request.POST.get('payment'))
        # exp = Expenses.objects.get(id=id)
        payment = Payment.objects.create(expense=expense)
        payment.save()
        return redirect('single-payments', expense.id)
    context = {
        'expense': expense,
        'payment_status': payment_status,
    }
    return render(request, 'payment/single.html', context)