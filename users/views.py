from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .forms import AddMoneyForm
from django_otp.plugins.otp_totp.models import TOTPDevice


User = get_user_model()

def signup_redirect(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create TOTP device for the new user
            device = TOTPDevice.objects.create(user=user, name='default', confirmed=True)

            # Generate OTP
            otp = device.token()

            # Send OTP via email
            send_mail(
                'Your verification code',
                f'Your OTP is: {otp}',
                'rdkhatwani07@gmail.com',
                [form.cleaned_data['email']],
            )
            request.session['otp_user'] = user.username
            # Redirect to OTP verification page
            return redirect('acc_otp')  
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def acc_otp(request):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        username = request.session.get('otp_user')  # store username in session during signup
        if not username:
            return redirect('signup_redirect')

        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username=username)
            device = TOTPDevice.objects.get(user=user, name='default')

            if device.verify(otp_entered):
                login(request, user)  # log the user in
                # delete session so user can't reuse OTP
                del request.session['otp_user']
                return redirect('home')
            else:
                return render(request, 'users/acc_otp.html', {'error': 'Invalid OTP!'})
        except Exception as e:
            return render(request, 'users/acc_otp.html', {'error': 'Something went wrong. Try again.'})
    
    return render(request, 'users/acc_otp.html')

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