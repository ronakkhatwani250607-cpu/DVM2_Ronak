from django.shortcuts import render
from .models import MetroLine, MetroStation

def home(request):
    return render(request, 'metro/home.html')

def stations_view(request):
    stations = MetroStation.objects.all().prefetch_related('lines')
    return render(request, 'metro/stations.html', {'stations': stations})

def lines_view(request):
    lines = MetroLine.objects.all()
    return render(request, 'metro/lines.html', {'lines': lines})