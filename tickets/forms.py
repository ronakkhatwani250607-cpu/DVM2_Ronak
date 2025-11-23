from django import forms
from .models import Ticket
from metro.models import MetroStation, MetroLine

class TicketPurchaseForm(forms.ModelForm):
    start_station = forms.ModelChoiceField(queryset=MetroStation.objects.all())
    end_station = forms.ModelChoiceField(queryset=MetroStation.objects.all())
    line = forms.ModelChoiceField(queryset=MetroLine.objects.all())

    class Meta:
        model = Ticket
        fields = ['start_station', 'end_station', 'line']