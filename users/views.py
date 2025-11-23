from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm
from django_otp.plugins.otp_totp.models import TOTPDevice




def signup_redirect(request):
    if request.method == "POST":
        return redirect('account_signup')
    return redirect('account_signup')

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})
@login_required
def add_money(request):
    if request.method == "POST":
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.wallet += amount
            request.user.save()
            return redirect('profile')  
    else:
        form = AddMoneyForm()
    return render(request, 'users/add_money.html', {'form': form})