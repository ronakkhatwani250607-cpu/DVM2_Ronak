
from django.urls import path
from . import views
urlpatterns=[
    path('buy/',views.buy_ticket,name='buy_ticket'),
    path('otp/',views.verify_otp,name='verify_otp'),
    path('my/',views.my_tickets,name='my_tickets'),
    path('scan/',views.scan_ticket,name='scan_ticket'),
]
