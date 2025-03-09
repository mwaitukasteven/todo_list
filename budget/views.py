from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Income, Expense

# Home Page

def homepage_view(request):
    return render(request, 'homepage.html')

def about(request):
    return render(request, 'about.html')

# Signup Page
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

# Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You logged in successfully')
            return redirect('dashboard')  # Redirect to dashboard on successful login
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

# Logout
def logout_view(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('homepage')

# Dashboard
@login_required
def dashboard_view(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    
    total_income = int(sum(income.amount for income in incomes))  # Convert to int
    total_expenses = int(sum(expense.amount for expense in expenses))  # Convert to int
    remaining_budget = total_income - total_expenses

    context = {
        'income': total_income,
        'expense': total_expenses,
        'remaining_budget': remaining_budget,
    }
    return render(request, 'dashboard.html', context)


# Add Income
@login_required
def add_income(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        Income.objects.create(user=request.user, amount=amount, description=description)
        messages.success(request, "Income added successfully.")
        return redirect('add_income')

    incomes = Income.objects.filter(user=request.user).order_by('-id')
    return render(request, 'add_income.html', {'incomes': incomes})

# Add Expense
@login_required
def add_expense(request):
    if request.method == 'POST':
        amount = float(request.POST.get('amount'))
        description = request.POST.get('description')

        # Calculate remaining budget
        incomes = Income.objects.filter(user=request.user)
        expenses = Expense.objects.filter(user=request.user)
        total_income = sum(income.amount for income in incomes)
        total_expenses = sum(expense.amount for expense in expenses)
        remaining_budget = total_income - total_expenses

        # Check if the expense exceeds the remaining budget
        if amount > remaining_budget:
            messages.error(request, "Expense exceeds the remaining budget. Please enter the correct amount")
            return redirect('add_expense')

        # If valid, save the expense
        Expense.objects.create(user=request.user, amount=amount, description=description)
        messages.success(request, "Expense added successfully.")
        return redirect('add_expense')

    expenses = Expense.objects.filter(user=request.user).order_by('-id')
    return render(request, 'add_expense.html', {'expenses': expenses})
