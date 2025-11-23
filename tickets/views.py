from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TicketPurchaseForm
from .models import Ticket
from django.core.mail import send_mail
from django.utils import timezone
import random

@login_required
def buy_ticket(request):
    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.passenger = request.user
            ticket.price = abs(ticket.start_station.id - ticket.end_station.id) * 10
            ticket.expiry_time = timezone.now() + timezone.timedelta(hours=6)
            if request.user.wallet >= ticket.price:
                request.user.wallet -= ticket.price
                request.user.save()
                ticket.otp = str(random.randint(100000, 999999))
                ticket.save()
                # send OTP to email (console backend prints it)
                send_mail('Your Metro Ticket OTP', f'OTP: {ticket.otp}', 'no-reply@metro.com', [request.user.email])
                return render(request, 'tickets/otp_verification.html', {'ticket_id': ticket.id})
            else:
                return render(request, 'tickets/buy_ticket.html', {'form': form, 'error': 'Insufficient money'})
    else:
        form = TicketPurchaseForm()
    return render(request, 'tickets/buy_ticket.html', {'form': form})

@login_required
def verify_otp(request):
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        otp_input = request.POST.get('otp')
        ticket = get_object_or_404(Ticket, id=ticket_id, passenger=request.user)
        if ticket.otp == otp_input and timezone.now() < ticket.expiry_time:
            ticket.otp_verified = True
            ticket.save()
            return redirect('my_tickets')
        else:
            return render(request, 'tickets/otp_result.html', {'message': 'Invalid or expired OTP'})
    return redirect('buy_ticket')

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(passenger=request.user).order_by('-created_at')
    return render(request, 'tickets/my_tickets.html', {'tickets': tickets})

@login_required
def scan_ticket(request):
    message = None
    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if ticket.status == 'active' and ticket.otp_verified:
                ticket.status = 'used'
                ticket.save()
                message = "Ticket scanned: allowed."
            else:
                message = f"Ticket not allowed: status={ticket.status}, otp_verified={ticket.otp_verified}"
        except Ticket.DoesNotExist:
            message = "Ticket not found."
    return render(request, 'tickets/scan_ticket.html', {'message': message})